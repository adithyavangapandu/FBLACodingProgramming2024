from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, jsonify)
from flask_login import current_user, login_required
from greenpot import db
from greenpot.models import Partner, Notification
from greenpot.partners.forms import PartnerForm, NotificationForm
from sqlalchemy import asc
from werkzeug.utils import secure_filename 
import os
import json
import io
import tempfile
import csv


partners = Blueprint('partners', __name__)




'''@partners.route("/update-")
def add_partners_from_csv():
    with open('/Users/adivangapandu/testdata.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Create a new Partner object for each row in the CSV
            partner = Partner(
                PartnerName=row['Partner Name'],
                Email=row['Contact Email'],
                ContactIndividual=row['Contact Individual'],
                PhoneNumber=row['Phone Number'],
                PartType=row['Partner Type'],
                Rsc=row['Resources'],
                money = row['Money'],
                time=row['Time'],
                timeframe=row['Timeframe'],
                user_id=current_user.id  # Assuming all partners have the same user_id
            )
            # Add the Partner object to the session
            db.session.add(partner)
    
    # Commit all changes to the database
    db.session.commit()
    return render_template('home.html') '''


@partners.route('/update-database', methods=['GET', 'POST'])
def add_partners_from_csv():
    if request.method == 'POST':
        file = request.files['csv_file']

        # Ensure a valid filename was submitted
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Ensure uploaded file is a CSV 
        if file and file.filename.lower().endswith('.csv'): 
            filename = secure_filename(file.filename)  # Sanitize the filename
            
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                # Save the file contents temporarily
                file.save(temp_file.name) 

            # Create the full save path and save the file


            # Open the saved file
                with open(temp_file.name, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # Create a new Partner object for each row in the CSV
                        partner = Partner(
                            PartnerName=row['Partner Name'],
                            Email=row['Contact Email'],
                            ContactIndividual=row['Contact Individual'],
                            PhoneNumber=row['Phone Number'],
                            PartType=row['Partner Type'],
                            Rsc=row['Resources'],
                            money = row['Money'],
                            time=row['Time'],
                            timeframe=row['Timeframe'],
                            user_id=current_user.id  # Assuming all partners have the same user_id
                        )
                        # Add the Partner object to the session
                        db.session.add(partner)
                
                # Commit all changes to the database
                    db.session.commit()
        return redirect(url_for('partners.partner'))
    else:
        return render_template('upload.html')

@partners.route("/clean-database")
def clean_partners():
    
    db.session.query(Partner).delete()
    # Commit all changes to the database
    db.session.commit()
    return render_template('home.html') 


@partners.route("/partner", methods=['GET', 'POST'])
def partner():
    if current_user.is_authenticated:
        partners = Partner.query.order_by(asc(Partner.PartnerName)).all()
    else:
        partners = []
    return render_template('search_partner.html', partners=partners, current_user_id=current_user.id)

@partners.route("/partner/user", methods=['GET', 'POST'])
def user_partner():
    if current_user.is_authenticated:
        partners = Partner.query.filter_by(user_id=current_user.id).order_by(asc(Partner.PartnerName)).all()
    else:
        partners = []

    return render_template('user_partner.html', partners=partners, current_user_id=current_user.id)



@partners.route('/partner/<int:partner_id>/view')
def view_partner(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    notification_form = NotificationForm()  # Create the form object

    return render_template('view_partner.html', partner=partner, notification_form=notification_form)

@partners.route('/create-reminder', methods=['POST'])
def create_reminder():
    form = NotificationForm()
    if form.validate_on_submit():
        reminder_type = form.reminder_type.data
        custom_message = form.custom_message.data
        partner_id = form.partner_id.data
        user_id=current_user.id

        # Create the notification object
        new_notification = Notification(
            user_id=user_id,
            partner_id=partner_id,
            reminder_type=reminder_type,
            message=custom_message 
        )

        # Add to the database session
        db.session.add(new_notification)

        # Commit the changes
        db.session.commit()
        
        flash('Reminder created successfully!', 'success')
        return redirect(request.referrer) # Redirect back
    else:
        # Handle form errors (you might want to render the modal again)
        flash('There were errors in your reminder form', 'danger')
        print(form.errors)
        return redirect(request.referrer)  # Redirect back to the previous page

# Display notifications
@partners.route('/fetch-notifications', methods=['GET'])
def fetch_notifications():
    if not current_user.is_authenticated:
        return jsonify([]) # Return empty array if not logged in

    user_notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.created_at.desc()).all()

    notifications_data = []
    for notif in user_notifications:
        notif_id = notif.id
        partner_name = getattr(notif.partner, 'PartnerName', None)
        reminder_type = getattr(notif, 'reminder_type', None)
        message = getattr(notif, 'message', None)
        is_read = notif.is_read
        created_at = notif.created_at.strftime('%Y-%m-%d %H:%M') if notif.created_at else None

        notification_entry = {
            'id': notif_id,
            'partner_id': notif.partner_id,
            'partnerName': partner_name,
            'reminderType': reminder_type,
            'is_read': is_read,
            'message': message,
            'createdAt': created_at
        }
        notifications_data.append(notification_entry)

    return jsonify(notifications_data)


@partners.route('/mark-notification-read/<int:notification_id>', methods=['PUT'])
def mark_notification_read(notification_id):
    notification_id = request.json['notification_id']

    # Fetch the notification by its ID
    notification = Notification.query.get(notification_id)

    if not notification:
        return jsonify({'error': 'Notification not found'}), 404

    # Update the is_read field to True
    notification.is_read = True

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'Notification marked as read successfully'}), 200




#Delete function
@partners.route('/partner/<int:partner_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_partner(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    if partner.user != current_user:
        abort(403)
    
    # Delete associated notifications
    notifications = Notification.query.filter_by(partner_id=partner_id).all()
    for notification in notifications:
        db.session.delete(notification)
    
    db.session.delete(partner)
    db.session.commit()
    flash('Partner Deleted.', 'success')
    return redirect(url_for('partners.partner'))


@partners.route('/partner/new', methods=['GET', 'POST'])
@login_required
def new_partner():
    form = PartnerForm()
    if form.validate_on_submit():
        partner = Partner(PartnerName=form.PartnerName.data,
                          Email=form.ContactEmail.data,
                          ContactIndividual=form.ContactIndividual.data,
                          PhoneNumber=form.PhoneNumber.data,
                          PartType=form.PartnerType.data,
                          Rsc=form.Resources.data,
                          money=form.Money.data,
                          time=form.NumTime.data,
                          timeframe=form.Timeframe.data,
                          Responsibilities=form.Responsibilities.data,
                          user=current_user)
        db.session.add(partner)
        db.session.commit()
        flash('The partner has been created!', 'success')
        return redirect(url_for('partners.partner'))
    return render_template('create_partner.html', title='New Partner', form=form, legend='New Partner')

#Update page
@partners.route('/partner/<int:partner_id>/update', methods=['GET','POST'])
@login_required
def update_partner(partner_id):
    print("Hello")
    partner = Partner.query.get_or_404(partner_id)
    if partner.user != current_user:
        abort(403)
    form = PartnerForm()
    # Making the changes to the database.

    if form.validate_on_submit():
        
        partner.PartnerName = form.PartnerName.data
        partner.Email = form.ContactEmail.data
        partner.ContactIndividual = form.ContactIndividual.data
        partner.PhoneNumber = form.PhoneNumber.data
        partner.PartType = form.PartnerType.data
        partner.Rsc = form.Resources.data
        partner.money = form.Money.data
        partner.time = form.NumTime.data
        partner.timeframe = form.Timeframe.data
        partner.Responsibilities = form.Responsibilities.data
        db.session.commit()
        flash('Information updated!', 'success')
        return redirect(url_for('partners.partner'))
    # Prepopulating the form.
    elif request.method == 'GET':
        form.PartnerName.data = partner.PartnerName
        form.ContactEmail.data = partner.Email
        form.ContactIndividual.data = partner.ContactIndividual
        form.PhoneNumber.data = partner.PhoneNumber
        form.PartnerType.data = partner.PartType
        form.Resources.data = partner.Rsc
        form.Money.data = partner.money
        form.NumTime.data = partner.time
        form.Timeframe.data = partner.timeframe
        form.Responsibilities.data = partner.Responsibilities

    # What is rendered when the button is clicked.
    return render_template('create_partner.html', title='Update Partner',
                           form=form, legend='Update Partner')



@partners.route('/report', methods=['GET'])
def report():
    # Get the list of visible partners from the query parameters
    visible_partners = request.args.get('visiblePartners')
    print(type(visible_partners))
    print(visible_partners)
    if visible_partners:
        visible_partners = json.loads(visible_partners)
    else:
        visible_partners = []
    partners = Partner.query.filter(Partner.PartnerName.in_(visible_partners)).all()
    print(partners)
    # Render the template and pass the visible partners data
    return render_template('report_partner.html', partners=partners, cur_id=current_user.id)




