import matplotlib.pyplot as plt


def plot_category_expenses(category_data):
    """
    Create a bar chart for category-wise expenses.
    """

    fig, ax = plt.subplots(figsize=(8, 5))

    category_data.plot(kind="bar", ax=ax)

    ax.set_title("Expenses by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")

    plt.xticks(rotation=45)

    plt.tight_layout()

    return fig


def plot_monthly_expenses(monthly_data):
    """
    Create a line chart for monthly expenses.
    """

    fig, ax = plt.subplots(figsize=(8, 5))

    monthly_data.plot(kind="line", marker="o", ax=ax)

    ax.set_title("Monthly Expense Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")

    plt.tight_layout()

    return fig


def plot_expense_distribution(category_data):
    """
    Create a pie chart showing expense distribution.
    """

    fig, ax = plt.subplots(figsize=(7, 7))

    category_data.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_ylabel("")

    ax.set_title("Expense Distribution")

    plt.tight_layout()

    return fig