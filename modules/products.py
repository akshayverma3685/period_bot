# modules/products.py

def get_product_suggestions() -> str:
    """
    Return a list of recommended menstrual health products.
    """
    products = [
        "🌸 Sanitary Pads – Ultra-soft & comfortable",
        "🌸 Menstrual Cups – Eco-friendly & reusable",
        "🌸 Heating Pad – For cramps relief",
        "🌸 Herbal Teas – For relaxation and pain relief",
        "🌸 Pain Relief Creams – For muscle relaxation"
    ]
    return "\n".join(products)

def get_self_care_tips() -> str:
    """
    Return daily self-care tips for periods.
    """
    tips = [
        "💧 Drink plenty of water to stay hydrated.",
        "🥗 Eat nutritious foods rich in iron and vitamins.",
        "🛌 Get enough rest and sleep.",
        "🏃 Gentle exercise like walking or stretching helps.",
        "🧘‍♀️ Practice relaxation techniques like meditation."
    ]
    return "\n".join(tips)
