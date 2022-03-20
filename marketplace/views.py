from flask import Blueprint, render_template, request, url_for, flash, redirect, abort
from .forms import SellShoes, PlaceBid, Search
from .models import Shoe, User, Bid
from . import db
from sqlalchemy import desc
from flask_login import login_user, login_required,logout_user, current_user
from datetime import datetime
import os
import secrets
from PIL import Image


bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
	shoes = db.session.query(Shoe).order_by(desc(Shoe.date_posted)).limit(5).all()
	form = Search()
	if form.validate_on_submit():
		search_query = form.search.data
		return redirect(url_for('main.search', query=search_query))

	return render_template('index.html', title = "Find Sneakers You'll Love <3", recent_shoes = shoes, form = form)


@bp.route('/search/<string:query>', methods=['GET', 'POST'])
def search(query):
	rendered_shoes = db.session.query(Shoe).filter(Shoe.brand == query).order_by(desc(Shoe.date_posted)).all()
	return render_template('search.html', title = 'Search Results', search_results = rendered_shoes, query=query)


@bp.route('/sell', methods=['GET', 'POST'])
def sell():
	if (not current_user.is_authenticated):
		flash(f'Please Login to Sell Shoes', 'Danger')
		return redirect(url_for('main.index'))

	form = SellShoes()
	if form.validate_on_submit():
		name = form.name.data
		brand = form.brand.data
		price = form.price.data
		size = form.size.data
		condition = form.condition.data
		colour_way = form.colour_way.data
		description = form.description.data
		style = form.style.data

		shoe = Shoe(name=name, brand=brand, price=price,condition=condition, colour_way=colour_way,description=description,style=style, size=size, image_file = 'uncLG.png', user_id=current_user.get_id())
		
		random_hex = secrets.token_hex(8)
		_, f_ext = os.path.splitext(form.image.data.filename)
		picture_fn = random_hex + f_ext
		picture_path = os.path.join(bp.root_path, 'static/img', picture_fn)

		i = Image.open(form.image.data)
		i.save(picture_path)
		shoe.image_file = picture_fn;

		db.session.add(shoe)
		db.session.commit()
		flash(f'Your item has been added to Sole', 'Success')
		return redirect(url_for('main.manage'))

	return render_template('sell.html', title = 'Sell Your Shoes', form = form)

@bp.route('/manage', methods=['GET', 'POST'])
def manage():
	if (not current_user.is_authenticated):
		flash(f'Please Login to Manage Your Shoes', 'Danger')
		return redirect(url_for('main.index'))

	shoes = User.query.get(current_user.get_id()).shoes
	return render_template('manage.html', title = 'Manage Bids', shoes = shoes)

@bp.route('/manage/<int:bid_id>/accept_bid', methods=['GET', 'POST'])
def accept_bid(bid_id):
	if (not current_user.is_authenticated):
		flash(f'Please Login to Manage Your Shoes', 'Danger')
		return redirect(url_for('main.index'))

	bid = Bid.query.get_or_404(bid_id)
	shoe = Shoe.query.get_or_404(bid.shoe_id)

	if shoe.seller != current_user:
		abort(403)

	bid.status = "Sold"
	shoe.sold_status = True
	bid.sold_date = datetime.now()
	db.session.commit()
	flash(f'Bid Accepted', 'Success')
	return redirect(url_for('main.manage'))


@bp.route('/manage/<int:bid_id>/reject_bid', methods=['GET', 'POST'])
def reject_bid(bid_id):
	if (not current_user.is_authenticated):
		flash(f'Please Login to Manage Your Shoes', 'Danger')
		return redirect(url_for('main.index'))

	bid = Bid.query.get_or_404(bid_id)
	shoe = Shoe.query.get_or_404(bid.shoe_id)

	if shoe.seller != current_user:
		abort(403)

	bid.status = "Rejected"
	shoe.sold_status = False
	db.session.commit()
	flash(f'Bid Rejected', 'Warning')
	return redirect(url_for('main.manage'))


@bp.route("/details/<int:shoe_id>", methods=['GET', 'POST'])
def details(shoe_id):
	shoe = Shoe.query.get_or_404(shoe_id)
	form = PlaceBid()
	if form.validate_on_submit():
		if (not current_user.is_authenticated):
			flash(f'Please Login to Place a Bid', 'Danger')
			return redirect(url_for('main.details', shoe_id=shoe.id))
		bid_amount = form.bid_amount.data
		phone_number = form.phone_number.data
		bid = Bid(amount=bid_amount, phone_number=phone_number, user_id=current_user.get_id(), shoe_id=shoe_id)
		db.session.add(bid)
		db.session.commit()
		flash(f'Your bid has been submitted', 'Success')
		return redirect(url_for('main.details', shoe_id=shoe.id))

	return render_template('details.html', title = shoe.name, shoe=shoe, form=form)


@bp.route("/history", methods=['GET', 'POST'])
def history():
	if (not current_user.is_authenticated):
		flash(f'Please Login to Manage Your Shoes', 'Danger')
		return redirect(url_for('main.index'))

	shoes = User.query.get(current_user.get_id()).shoes
	return render_template('history.html', title = 'Previous Sales', shoes = shoes)


@bp.errorhandler(404)
def not_found(e):
        return render_template('error_404.html'), 404

@bp.errorhandler(500)
def server_error(e):
        return render_template('error_500.html')
