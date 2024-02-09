from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from greenpot import db
from greenpot.models import Partner
from greenpot.partners.forms import PartnerForm
from sqlalchemy import asc
import json
import csv


partners = Blueprint('partners', __name__)




@partners.route("/update-database")
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
                user_id=2  # Assuming all partners have the same user_id
            )
            # Add the Partner object to the session
            db.session.add(partner)
    
    # Commit all changes to the database
    db.session.commit()
    return render_template('home.html')

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

@partners.route('/partner/new', methods=['GET', 'POST'])
@login_required
def new_partner():
    form = PartnerForm()
    if form.validate_on_submit():
        partner = Partner(PartnerName = form.PartnerName.data,
                          Email = form.ContactEmail.data,
                          ContactIndividual = form.ContactIndividual.data,
                          PhoneNumber = form.PhoneNumber.data,
                          #Drop down box - Business or Community
                          PartType = form.PartnerType.data,
                          Rsc = form.Resources.data,
                          user = current_user)
        db.session.add(partner)
        db.session.commit()
        flash('The partner has been created!', 'success')
        return redirect(url_for('partners.partner'))
    return render_template('create_partner.html', title='New Partner', form=form,
                           legend='New Partner')


@partners.route('/partner/<int:partner_id>/view')
def view_partner(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    return render_template('view_partner.html', partner=partner)




#Delete function
@partners.route('/partner/<int:partner_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_partner(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    if partner.user != current_user:
        abort(403)
    db.session.delete(partner)
    db.session.commit()
    flash('Partner Deleted.', 'success')
    return redirect(url_for('partners.partner'))



#Update page
@partners.route('/partner/<int:partner_id>/update', methods=['GET','POST'])
@login_required
def update_partner(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    if partner.user != current_user:
        abort(403)
    form = PartnerForm()
    #Making the changes to the database.
    if form.validate_on_submit():
        partner.PartnerName = form.PartnerName.data
        partner.Email = form.ContactEmail.data
        partner.ContactIndividual = form.ContactIndividual.data
        partner.PhoneNumber = form.PhoneNumber.data
        partner.PartType = form.PartnerType.data
        partner.Rsc = form.Resources.data
        db.session.commit()
        flash('Information updated!', 'success')
        return redirect(url_for('partners.partner'))
    #Prepopulating the form.
    elif request.method == 'GET':
        form.PartnerName.data = partner.PartnerName
        form.ContactEmail.data = partner.Email
        form.ContactIndividual.data = partner.ContactIndividual
        form.PhoneNumber.data = partner.PhoneNumber
        form.PartnerType.data = partner.PartType
        form.Resources.data = partner.Rsc
    #What is rendered when the button is clicked.
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




