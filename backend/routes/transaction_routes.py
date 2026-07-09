from datetime import datetime
from collections import defaultdict

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..auth import login_required

from ..models import db
from ..models.transaction import Transaction


transaction_bp = Blueprint("transaction", __name__)

def validate_transaction_form(form):

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="transactions"
    )

    title = form.get("title", "").strip()

    amount_text = form.get("amount", "").strip()

    category = form.get("category", "").strip()

    transaction_type = form.get(
        "transaction_type",
        ""
    ).strip()

    date_text = form.get("date", "").strip()

    description = form.get(
        "description",
        ""
    ).strip()


    if not title:

        return None, "Title is required."


    try:

        amount = float(amount_text)

    except ValueError:

        return None, "Amount must be a valid number."


    if amount <= 0:

        return None, "Amount must be greater than zero."


    allowed_categories = {
        "Food",
        "Travel",
        "Shopping",
        "Rent",
        "Bills",
        "Salary",
        "Other"
    }


    if category not in allowed_categories:

        return None, "Please select a valid category."


    allowed_types = {
        "Income",
        "Expense"
    }


    if transaction_type not in allowed_types:

        return None, "Please select a valid transaction type."


    try:

        transaction_date = datetime.strptime(
            date_text,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        return None, "Please enter a valid date."


    cleaned_data = {

        "title": title,

        "amount": amount,

        "category": category,

        "transaction_type": transaction_type,

        "date": transaction_date,

        "description": description

    }


    return cleaned_data, None


@transaction_bp.route("/")
@login_required
def dashboard():

    search = request.args.get("search", "").strip()

    transaction_type = request.args.get(
        "type",
        ""
    ).strip()

    category = request.args.get(
        "category",
        ""
    ).strip()


    query = Transaction.query.filter_by(
        user_id=session["user_id"]
    )


    if search:

        search_pattern = f"%{search}%"

        query = query.filter(

            db.or_(

                Transaction.title.ilike(search_pattern),

                Transaction.description.ilike(search_pattern)

            )

        )


    if transaction_type:

        query = query.filter_by(
            transaction_type=transaction_type
        )


    if category:

        query = query.filter_by(
            category=category
        )


    transactions = query.order_by(

        Transaction.date.desc(),

        Transaction.id.desc()

    ).all()


    total_income = sum(

        transaction.amount

        for transaction in transactions

        if transaction.transaction_type == "Income"

    )


    total_expenses = sum(

        transaction.amount

        for transaction in transactions

        if transaction.transaction_type == "Expense"

    )


    balance = total_income - total_expenses


    # -----------------------------------
    # CATEGORY-WISE EXPENSE DATA
    # -----------------------------------

    category_expenses = defaultdict(float)


    for transaction in transactions:

        if transaction.transaction_type == "Expense":

            category_expenses[
                transaction.category
            ] += transaction.amount


    category_labels = list(
        category_expenses.keys()
    )


    category_values = list(
        category_expenses.values()
    )


    # -----------------------------------
    # MONTHLY INCOME AND EXPENSE DATA
    # -----------------------------------

    monthly_data = defaultdict(
        lambda: {
            "income": 0,
            "expense": 0
        }
    )


    for transaction in transactions:

        month_key = transaction.date.strftime(
            "%Y-%m"
        )


        if transaction.transaction_type == "Income":

            monthly_data[
                month_key
            ]["income"] += transaction.amount


        elif transaction.transaction_type == "Expense":

            monthly_data[
                month_key
            ]["expense"] += transaction.amount


    sorted_months = sorted(
        monthly_data.keys()
    )


    monthly_labels = [

        datetime.strptime(
            month,
            "%Y-%m"
        ).strftime("%b %Y")

        for month in sorted_months

    ]


    monthly_income = [

        monthly_data[
            month
        ]["income"]

        for month in sorted_months

    ]


    monthly_expenses = [

        monthly_data[
            month
        ]["expense"]

        for month in sorted_months

    ]


    return render_template(

        "dashboard.html",

        transactions=transactions,

        total_income=total_income,

        total_expenses=total_expenses,

        balance=balance,

        search=search,

        selected_type=transaction_type,

        selected_category=category,

        category_labels=category_labels,

        category_values=category_values,

        monthly_labels=monthly_labels,

        monthly_income=monthly_income,

        monthly_expenses=monthly_expenses

    )

@transaction_bp.route(
    "/add-transaction",
    methods=["GET", "POST"]
)
@login_required
def add_transaction():

    if request.method == "POST":

        data, error = validate_transaction_form(
            request.form
        )


        if error:

            flash(error, "error")

            return render_template(
                "add_transaction.html"
            )


        new_transaction = Transaction(
            **data,
            user_id=session["user_id"]
        )


        db.session.add(new_transaction)

        db.session.commit()


        flash(
            "Transaction added successfully.",
            "success"
        )


        return redirect(
            url_for("transaction.dashboard")
        )


    return render_template(
        "add_transaction.html"
    )

@transaction_bp.route(
    "/edit-transaction/<int:transaction_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_transaction(transaction_id):

    transaction = Transaction.query.filter_by(
        id=transaction_id,
        user_id=session["user_id"]
    ).first_or_404()


    if request.method == "POST":

        data, error = validate_transaction_form(
            request.form
        )


        if error:

            flash(error, "error")

            return render_template(
                "edit_transaction.html",
                transaction=transaction
            )


        transaction.title = data["title"]

        transaction.amount = data["amount"]

        transaction.category = data["category"]

        transaction.transaction_type = data[
            "transaction_type"
        ]

        transaction.date = data["date"]

        transaction.description = data[
            "description"
        ]


        db.session.commit()


        flash(
            "Transaction updated successfully.",
            "success"
        )


        return redirect(
            url_for("transaction.dashboard")
        )


    return render_template(
        "edit_transaction.html",
        transaction=transaction
    )

@transaction_bp.route(
    "/delete-transaction/<int:transaction_id>",
    methods=["POST"]
)
@login_required
def delete_transaction(transaction_id):

    transaction = Transaction.query.filter_by(
        id=transaction_id,
        user_id=session["user_id"]
    ).first_or_404()


    db.session.delete(transaction)

    db.session.commit()


    flash(
        "Transaction deleted successfully.",
        "success"
    )


    return redirect(
        url_for("transaction.dashboard")
    )