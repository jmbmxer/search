#!/usr/bin/env python

import datetime

from flask import Blueprint, render_template, flash, redirect, request, session, url_for, jsonify
from urlparse import urlparse
from flask_application import app
from flask.ext.security import *
import stripe

# -- ported --#
from functools import wraps
from flask_application.forms import RegisterForm, LoginForm, PostLink, PostGroup
from flask_application.models import *
from sqlalchemy.exc import *
from flask_application.xgoogle.search import GoogleSearch, SearchError

#from config import stripe_keys
#from flask_application.config import DEFAULT_SMALL_AMOUNT, DEFAULT_SMALL_DESCRIPTION, DEFAULT_LARGE_AMOUNT, DEFAULT_LARGE_DESCRIPTION

stripe.api_key = app.config['SECRET_KEY']

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    return render_template(
                'index.html',
                config=app.config,
                now=datetime.datetime.now,
            )
@app.route('/pricing' ,methods=['GET'])
def pricing():
    """handles our message notification"""
    return render_template('pricing.html')

@frontend.route('/profile')
@login_required
def profile():
    return render_template(
        'profiles/profile.html',
        content='Profile Page')

#-- Handle Payments with Stripe--#

"""
@app.route('/charge', methods=['POST'])
def charge():

  customer_email = request.form['email']



  customer = stripe.Customer.create(
          email=customer_email,
          card=request.form['stripeToken']
          )

  customer_id = customer.id

    # save the customer ID in DB for later use
  save_stripe_customer(customer_email, customer_id)

  # charge the customer (new or already present in DB)
  charge_valid, charge_msg = stripe_charge(customer_id)

  return render_template('charge.html',
          amount_usd=get_amount_usd(),
          customer_email=customer_email,
          charge_valid=charge_valid,
          charge_msg=charge_msg)
"""


"""@frontend.route('/small', methods=['GET', 'POST'])
def small():
        return render_template('small.html',
          key = app.config['PUBLISHABLE_KEY'],
          amount_usd=get_amount_usd()
          )
def get_amount_usd(amount=525):
    return float(amount) / 100

def get_stripe_customer(customer_email):


  customer_info = User.query.filter_by(email=customer_email).all

  if(customer_info == None):
    return False, customer_info
  else:
    return True, customer_info

def save_stripe_customer(customer_email, customer_id):

  # If already have a customer by that email, delete old entry
  reply, entry = get_stripe_customer(customer_email)
  if(reply):
    return "your already have an account with us! Log in to upgrade."
  else:
    if form.validate_on_submit():
      new_user = User(
                         form.group.data,
                         uid,
                         )
              db.session.flush()
              db.session.add(new_user)
              db.session.commit()
              flash("!")
"""


#-- ported from og template -- #

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,error), 'error')


@frontend.route('/')
def home():
  return render_template('home.html')


"""@frontend.route('/registertest/', methods=['GET', 'POST'])

def registertest():
    Registers the user.
    error=None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                 '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif request.form['username'] is not None:
            error = 'The username is already taken'
        else:
           if form.validate_on_submit():
            pw_hash=generate_password_hash(request.form['password'])
            username=request.form['username']
            email=request.form['email']
            level=0
            new_user = User(
                         username,
                         email,
                         uid,
                         )
            db.session.flush()
            db.session.add(new_group)
            db.session.commit()

            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('registertest.html', error=error)"""

# Generate Google search Query URL for demo
@frontend.route('/demo/', methods=['GET', 'POST'])
def generateurldemo():
  error=None
  uid = User.query.get(32)

  form = PostLink(request.form, csrf_enabled = False)
  groups = Groups.query.filter_by(user_id=uid.id).all()


  if request.method=='POST':
    flash("You created a custom google search!")
    group_passed = request.form['grp']
    search_passed = request.form['srch']
    links = Links.query.filter_by(author_id=uid.id,group_id=group_passed)
    out_str = ' '
    for link in links:
      out_str += 'site%3A'+link.link+'+OR+'
     #grab final
    final = 'https://www.google.com/search?q='+search_passed+out_str
    #Use this for API
    #return redirect(final, 301)
    return render_template('demo.html', form=form, groups=groups, group_passed=group_passed, search_passed=search_passed, links=links, out_str=out_str, final=final)

  else:
    goog_url = 'GET'
    return render_template('demo.html', goog_url = goog_url, form=form, groups=groups)

@frontend.route('/groups/', methods=['GET','POST'])
@login_required
def members():
    error=None
    form = PostGroup(request.form, csrf_enabled = False)
    uid = session['user_id']
    groups = Groups.query.filter_by(user_id=uid).all()

    for group in groups:
      if request.method=='POST':
          if form.validate_on_submit():
            if form.group.data == group.name:
              flash('That group already exists!')
              return render_template('members.html', form=form, error=error, groups=groups)
            else:
              new_group = Groups(
                         form.group.data,
                         uid,
                         )
              db.session.flush()
              db.session.add(new_group)
              db.session.commit()
              flash("You created a group, time to add some links!")
              return redirect(url_for('.members'))
          else:
              flash("That group didn't work, maybe the name is too long?")
              return redirect(url_for('.members'))
              #flash_errors(form)

    if request.method=='POST':
          if form.validate_on_submit():
              new_group = Groups(
                         form.group.data,
                         uid,
                         )
              db.session.flush()
              db.session.add(new_group)
              db.session.commit()
              # db.session.flush()
              flash("You have created your first group!")
              return redirect(url_for('.members'))
          else:
              flash_errors(form)
    return render_template('members.html', form=form, error=error, groups=groups)

@frontend.route('/groups/<group>', methods=['GET','POST'])
@login_required
def memberextend(group):
    error=None
    form = PostLink(request.form, csrf_enabled = False)
    uid = session['user_id']
    groups = Groups.query.filter_by(user_id=uid)
    links = Links.query.filter_by(author_id=uid,group_id=group)

    for link in links:
      #return group
      if request.method=='POST':
          if form.validate_on_submit():
             if form.link.data == link.link:
                flash('That link already exists!')
                return render_template('add_link.html', form=form, error=error, tester = group, uid=uid, groups=groups, links=links)
             else:
              new_link = Links(
                         uid,
                         form.link.data,
                         group,
                         )
             db.session.add(new_link)
             db.session.commit()

             flash("You have added a link!")
             return redirect('/groups/'+group)
          else:
           flash_errors(form)
    if request.method=='POST':
      if form.validate_on_submit():
            new_link = Links(
                       uid,
                       form.link.data,
                       group,
                     )
            db.session.add(new_link)
            db.session.commit()
            flash("You have added your first link!")
            return redirect('/groups/'+group)
      else:
           flash_errors(form)
    return render_template('add_link.html', form=form, error=error, tester = group, uid=uid, groups=groups, links=links)

#Delete group functionality
@frontend.route('/<group_to_delete>/deletegroup/', methods=['POST'])
@login_required
def deletegroup(group_to_delete):
    error=None
    uid = session['user_id']
    groups = Groups.query.filter_by(user_id=uid, name =group_to_delete)
    links = Links.query.filter_by(author_id=uid,group_id=group_to_delete)
    for group in groups:
      db.session.delete(group)
      for link in links:
        db.session.delete(link)
    db.session.commit()
    return redirect(url_for('.members'))

#Delete link functionality
@frontend.route('/<link_to_delete>/deletelink/', methods=['POST'])
@login_required
def deletelink(link_to_delete):

    error=None
    uid = session['user_id']
    links = Links.query.filter_by(author_id=uid,link=link_to_delete)
    for link in links:
      #return group.name
      db.session.delete(link)

      db.session.commit()
      return redirect(url_for('.members', group=link_to_delete))

# Generate Google search Query URL
@frontend.route('/search/', methods=['GET', 'POST'])
@login_required
def generateurl():
  error=None
  uid = session['user_id']
  form = PostLink(request.form, csrf_enabled = False)
  groups = Groups.query.filter_by(user_id=uid).all()


  if request.method=='POST':
    flash("You created a custom google search!")
    group_passed = request.form['grp']
    search_passed = request.form['srch']
    links = Links.query.filter_by(author_id=uid,group_id=group_passed)
    out_str = ' '
    for link in links:
      out_str += 'site%3A'+link.link+'+OR+'
     #grab final
    final = 'https://www.google.com/search?q='+search_passed+out_str
    return render_template('generator.html', form=form, groups=groups, group_passed=group_passed, search_passed=search_passed, links=links, out_str=out_str, final=final)

  else:
    goog_url = 'GET'
    return render_template('generator.html', goog_url = goog_url, form=form, groups=groups)


# Trying out xgooglesearch python script

# Generate Google search Query URL
"""@frontend.route('/searchit/', methods=['GET', 'POST'])
@login_required
def generateurl2():
  error=None
  uid = session['user_id']
  form = PostLink(request.form, csrf_enabled = False)
  groups = Groups.query.filter_by(user_id=uid).all()



  if request.method=='POST':
    flash("You created a custom google search!")
    group_passed = request.form['grp']
    search_passed = request.form['srch']
    links = Links.query.filter_by(author_id=uid,group_id=group_passed)
    out_str = ' '
    for link in links:
      out_str += 'site%3A'+link.link+'+OR+'
     #grab final
    final = 'https://www.google.com/search?q='+search_passed+out_str
    semi_final = search_passed+out_str

    gs = GoogleSearch(semi_final)
    gs.results_per_page=50
    results = gs.get_results()


    return render_template('generator.html', form=form, groups=groups, group_passed=group_passed, search_passed=search_passed, links=links, out_str=out_str, final=final, results=results, semi_final=semi_final)

  else:
    goog_url = 'GET'
    return render_template('generator.html', goog_url = goog_url, form=form, groups=groups)"""




# Error handling

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404
