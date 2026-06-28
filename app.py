import streamlit as st
import math

st.set_page_config(
    page_title="Index CFD Position Size Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
    }
    .critical-box {
        background-color: #f8d7da;
        border: 1px solid #dc3545;
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #28a745;
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ===================== BROKER SPECS =====================
BROKER_SPECS = {
    "GENERIC": {
        "US500": {"name": "S&P 500", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 0.5, "margin_pct": 5.0, "swap_long": -2.50, "swap_short": -1.50, "commission_per_lot": 0.0, "currency": "USD"},
        "US30": {"name": "Dow Jones 30", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 2.0, "margin_pct": 5.0, "swap_long": -3.00, "swap_short": -2.00, "commission_per_lot": 0.0, "currency": "USD"},
        "USTEC": {"name": "NASDAQ 100", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 1.0, "margin_pct": 5.0, "swap_long": -2.00, "swap_short": -1.00, "commission_per_lot": 0.0, "currency": "USD"},
        "US2000": {"name": "Russell 2000", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 0.3, "margin_pct": 5.0, "swap_long": -1.50, "swap_short": -1.00, "commission_per_lot": 0.0, "currency": "USD"},
        "DE40": {"name": "DAX 40", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 1.0, "margin_pct": 5.0, "swap_long": -2.50, "swap_short": -1.50, "commission_per_lot": 0.0, "currency": "EUR"},
        "EU50": {"name": "EURO STOXX 50", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 0.8, "margin_pct": 5.0, "swap_long": -1.80, "swap_short": -1.20, "commission_per_lot": 0.0, "currency": "EUR"},
        "UK100": {"name": "FTSE 100", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 1.0, "margin_pct": 5.0, "swap_long": -2.00, "swap_short": -1.50, "commission_per_lot": 0.0, "currency": "GBP"},
        "FR40": {"name": "CAC 40", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 1.0, "margin_pct": 5.0, "swap_long": -1.50, "swap_short": -1.00, "commission_per_lot": 0.0, "currency": "EUR"},
        "ES35": {"name": "IBEX 35", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 3.0, "margin_pct": 5.0, "swap_long": -1.50, "swap_short": -1.00, "commission_per_lot": 0.0, "currency": "EUR"},
        "STOXX600": {"name": "STOXX Europe 600", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 0.3, "margin_pct": 5.0, "swap_long": -1.20, "swap_short": -0.80, "commission_per_lot": 0.0, "currency": "EUR"},
        "JP225": {"name": "Nikkei 225", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 5.0, "margin_pct": 5.0, "swap_long": -5.00, "swap_short": -3.00, "commission_per_lot": 0.0, "currency": "JPY"},
        "HK50": {"name": "Hang Seng Index", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 5.0, "margin_pct": 5.0, "swap_long": -8.00, "swap_short": -5.00, "commission_per_lot": 0.0, "currency": "HKD"},
        "AUS200": {"name": "ASX 200", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 1.0, "margin_pct": 5.0, "swap_long": -2.50, "swap_short": -1.50, "commission_per_lot": 0.0, "currency": "AUD"},
        "CN50": {"name": "China A50", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 2.0, "margin_pct": 5.0, "swap_long": -3.00, "swap_short": -2.00, "commission_per_lot": 0.0, "currency": "USD"},
        "IN50": {"name": "NIFTY 50", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 2.0, "margin_pct": 5.0, "swap_long": -2.00, "swap_short": -1.50, "commission_per_lot": 0.0, "currency": "INR"},
        "KR200": {"name": "KOSPI 200", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 0.1, "margin_pct": 5.0, "swap_long": -1.50, "swap_short": -1.00, "commission_per_lot": 0.0, "currency": "KRW"},
        "SG30": {"name": "Straits Times Index", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 0.5, "margin_pct": 5.0, "swap_long": -1.50, "swap_short": -1.00, "commission_per_lot": 0.0, "currency": "SGD"},
    },
    "RAW_SPREAD": {
        "US500": {"name": "S&P 500", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 0.2, "margin_pct": 5.0, "swap_long": -2.50, "swap_short": -1.50, "commission_per_lot": 3.50, "currency": "USD"},
        "US30": {"name": "Dow Jones 30", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 1.0, "margin_pct": 5.0, "swap_long": -3.00, "swap_short": -2.00, "commission_per_lot": 3.50, "currency": "USD"},
        "USTEC": {"name": "NASDAQ 100", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 0.5, "margin_pct": 5.0, "swap_long": -2.00, "swap_short": -1.00, "commission_per_lot": 3.50, "currency": "USD"},
        "DE40": {"name": "DAX 40", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 0.5, "margin_pct": 5.0, "swap_long": -2.50, "swap_short": -1.50, "commission_per_lot": 3.50, "currency": "EUR"},
        "UK100": {"name": "FTSE 100", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 0.5, "margin_pct": 5.0, "swap_long": -2.00, "swap_short": -1.50, "commission_per_lot": 3.50, "currency": "GBP"},
        "JP225": {"name": "Nikkei 225", "lot_size": 1.0, "point_value_per_lot": 1.0, "min_lot": 0.01, "max_lot": 500.0, "lot_step": 0.01, "spread_points": 3.0, "margin_pct": 5.0, "swap_long": -5.00, "swap_short": -3.00, "commission_per_lot": 3.50, "currency": "JPY"},
    },
}

def calculate_cfd_position_size(account_balance, risk_percent, entry_price, stop_loss_price, 
                                   index_code="US500", broker="GENERIC", direction="LONG", 
                                   target_price=None, holding_days=1):
    specs = BROKER_SPECS[broker][index_code]

    lot_size = specs["lot_size"]
    point_value = specs["point_value_per_lot"]
    min_lot = specs["min_lot"]
    max_lot = specs["max_lot"]
    lot_step = specs["lot_step"]
    spread = specs["spread_points"]
    margin_pct = specs["margin_pct"]
    swap_long = specs["swap_long"]
    swap_short = specs["swap_short"]
    commission = specs["commission_per_lot"]
    currency = specs["currency"]

    dollar_risk = account_balance * (risk_percent / 100.0)
    price_distance = abs(entry_price - stop_loss_price)

    if direction == "LONG":
        effective_entry = entry_price + spread
        swap_per_lot = swap_long
    else:
        effective_entry = entry_price - spread
        swap_per_lot = swap_short

    dollar_risk_per_lot = price_distance * point_value
    total_commission_per_lot = commission * 2
    spread_cost_per_lot = spread * point_value
    total_entry_cost_per_lot = spread_cost_per_lot + total_commission_per_lot
    effective_risk_per_lot = dollar_risk_per_lot + total_entry_cost_per_lot

    if effective_risk_per_lot <= 0:
        return None

    raw_lots = dollar_risk / effective_risk_per_lot
    lots = math.floor(raw_lots / lot_step) * lot_step
    lots = max(min_lot, min(lots, max_lot))
    lots = round(lots, int(-math.log10(lot_step)))

    notional_value = entry_price * lot_size * lots * point_value
    margin_required = notional_value * (margin_pct / 100.0)
    total_risk_amount = lots * effective_risk_per_lot
    actual_risk_pct = (total_risk_amount / account_balance) * 100 if account_balance > 0 else 0
    total_swap = lots * swap_per_lot * holding_days
    total_spread_cost = lots * spread_cost_per_lot
    total_commission = lots * total_commission_per_lot
    leverage = 100.0 / margin_pct if margin_pct > 0 else 0

    rr_ratio = None
    rr_text = "N/A"
    reward_amount = 0
    breakeven_winrate = None

    if target_price is not None:
        reward_distance = abs(target_price - entry_price)
        reward_amount = lots * reward_distance * point_value
        rr_ratio = reward_distance / price_distance if price_distance > 0 else 0
        rr_text = f"1:{rr_ratio:.2f}"
        breakeven_winrate = (1 / (1 + rr_ratio)) * 100 if rr_ratio > 0 else 0

    return {
        "index": specs["name"],
        "index_code": index_code,
        "broker_profile": broker,
        "currency": currency,
        "direction": direction,
        "account_balance": account_balance,
        "risk_percent": risk_percent,
        "entry_price": entry_price,
        "stop_loss_price": stop_loss_price,
        "target_price": target_price,
        "holding_days": holding_days,
        "lot_size": lot_size,
        "point_value_per_lot": point_value,
        "min_lot": min_lot,
        "max_lot": max_lot,
        "lot_step": lot_step,
        "spread_points": spread,
        "margin_pct": margin_pct,
        "leverage": leverage,
        "swap_per_lot": swap_per_lot,
        "commission_per_lot": commission,
        "dollar_risk_allowed": round(dollar_risk, 2),
        "price_distance": round(price_distance, 2),
        "effective_entry": round(effective_entry, 2),
        "dollar_risk_per_lot": round(dollar_risk_per_lot, 2),
        "spread_cost_per_lot": round(spread_cost_per_lot, 2),
        "commission_per_lot_roundtrip": round(total_commission_per_lot, 2),
        "effective_risk_per_lot": round(effective_risk_per_lot, 2),
        "raw_lots": round(raw_lots, 4),
        "lots": lots,
        "notional_value": round(notional_value, 2),
        "margin_required": round(margin_required, 2),
        "margin_pct_of_account": round((margin_required / account_balance) * 100, 2) if account_balance > 0 else 0,
        "total_spread_cost": round(total_spread_cost, 2),
        "total_commission": round(total_commission, 2),
        "total_swap": round(total_swap, 2),
        "total_risk_amount": round(total_risk_amount, 2),
        "actual_risk_pct": round(actual_risk_pct, 2),
        "reward_amount": round(reward_amount, 2) if target_price else 0,
        "rr_ratio": round(rr_ratio, 2) if rr_ratio else None,
        "rr_text": rr_text,
        "breakeven_winrate": round(breakeven_winrate, 1) if breakeven_winrate else None,
        "margin_warning": margin_required > account_balance * 0.5,
        "risk_warning": actual_risk_pct > risk_percent * 1.1,
        "insufficient_margin": margin_required > account_balance,
        "zero_position": lots <= 0,
    }

# ===================== UI =====================

st.markdown('<div class="main-header">📊 Index CFD Position Size Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Calculate optimal position sizing for index CFD trading with risk management</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    broker = st.selectbox("Broker Profile", ["GENERIC", "RAW_SPREAD"], 
                         help="GENERIC = spread-only (IG, Plus500). RAW_SPREAD = tight spread + commission (IC Markets, Pepperstone)")

    available_indices = list(BROKER_SPECS[broker].keys())
    index_code = st.selectbox("Index", available_indices, 
                              format_func=lambda x: f"{x} - {BROKER_SPECS[broker][x]['name']}")

    direction = st.radio("Direction", ["LONG", "SHORT"], horizontal=True)

    st.divider()
    st.caption("💡 **Tip:** Verify these specs with your actual broker. Spreads, swaps, and margin vary.")

# Main content - split into columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💰 Account & Risk")
    account_balance = st.number_input("Account Balance", min_value=100.0, value=10000.0, step=100.0, format="%.2f")
    risk_percent = st.slider("Risk per Trade (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

    st.subheader("📈 Trade Parameters")
    entry_price = st.number_input("Entry Price", min_value=0.01, value=4500.0, step=1.0, format="%.2f")
    stop_loss_price = st.number_input("Stop Loss Price", min_value=0.01, value=4485.0, step=1.0, format="%.2f")
    target_price = st.number_input("Target Price (optional)", min_value=0.0, value=4545.0, step=1.0, format="%.2f")

    if target_price == 0:
        target_price = None

    holding_days = st.number_input("Holding Days (for swap calc)", min_value=0, max_value=365, value=1, step=1)

with col2:
    st.subheader("🔧 Contract Specs")
    specs = BROKER_SPECS[broker][index_code]

    st.metric("Index", specs["name"])
    st.metric("Currency", specs["currency"])
    st.metric("Point Value", f"{specs['currency']} {specs['point_value_per_lot']} per lot")
    st.metric("Spread", f"{specs['spread_points']} points")
    st.metric("Margin", f"{specs['margin_pct']}% ({100/specs['margin_pct']:.0f}:1 leverage)")
    st.metric("Min/Max Lot", f"{specs['min_lot']} / {specs['max_lot']}")

    if specs["commission_per_lot"] > 0:
        st.metric("Commission", f"{specs['currency']} {specs['commission_per_lot']}/lot per side")
    else:
        st.metric("Commission", "Spread only")

# Calculate button
st.divider()
if st.button("🚀 Calculate Position Size", type="primary", use_container_width=True):
    result = calculate_cfd_position_size(
        account_balance=account_balance,
        risk_percent=risk_percent,
        entry_price=entry_price,
        stop_loss_price=stop_loss_price,
        index_code=index_code,
        broker=broker,
        direction=direction,
        target_price=target_price,
        holding_days=holding_days
    )

    if result is None:
        st.error("❌ Invalid input. Check your stop loss placement.")
    else:
        # Warnings
        if result["insufficient_margin"]:
            st.markdown(f'<div class="critical-box">❌ <b>CRITICAL:</b> Insufficient margin! You need {result["currency"]} {result["margin_required"]:,.2f} but only have {result["currency"]} {result["account_balance"]:,.2f}.</div>', unsafe_allow_html=True)
        elif result["margin_warning"]:
            st.markdown(f'<div class="warning-box">⚠️ <b>WARNING:</b> Margin requirement ({result["margin_pct_of_account"]:.1f}%) exceeds 50% of your account. Consider reducing position size or adding funds.</div>', unsafe_allow_html=True)

        if result["risk_warning"]:
            st.markdown(f'<div class="warning-box">⚠️ <b>WARNING:</b> Actual risk ({result["actual_risk_pct"]:.2f}%) exceeds your target ({result["risk_percent"]:.2f}%).</div>', unsafe_allow_html=True)

        if result["zero_position"]:
            st.markdown(f'<div class="warning-box">⚠️ <b>WARNING:</b> Position size is 0. Your stop loss is too wide for your risk parameters. Tighten your stop or increase risk %.</div>', unsafe_allow_html=True)

        # Main result
        st.divider()
        st.markdown(f'<div class="success-box" style="text-align:center;"><h2>📍 Recommended Position: {result["lots"]} LOTS</h2></div>', unsafe_allow_html=True)

        # Metrics grid
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Notional Value", f"{result['currency']} {result['notional_value']:,.0f}")
        with m2:
            st.metric("Margin Required", f"{result['currency']} {result['margin_required']:,.2f}")
        with m3:
            st.metric("Total Risk", f"{result['currency']} {result['total_risk_amount']:,.2f}")
        with m4:
            st.metric("Actual Risk %", f"{result['actual_risk_pct']:.2f}%")

        # Detailed breakdown
        st.divider()
        st.subheader("📋 Detailed Breakdown")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**Risk Calculation**")
            st.write(f"• Max Dollar Risk Allowed: {result['currency']} {result['dollar_risk_allowed']:,.2f}")
            st.write(f"• Price Distance: {result['price_distance']:.2f} points")
            st.write(f"• Effective Entry: {result['effective_entry']:.2f} (incl. spread)")
            st.write(f"• Risk per Lot: {result['currency']} {result['dollar_risk_per_lot']:,.2f}")
            st.write(f"• + Spread Cost: {result['currency']} {result['spread_cost_per_lot']:,.2f}")
            st.write(f"• + Commission (RT): {result['currency']} {result['commission_per_lot_roundtrip']:,.2f}")
            st.write(f"• = Effective Risk/Lot: **{result['currency']} {result['effective_risk_per_lot']:,.2f}**")
            st.write(f"• Raw Lots: {result['raw_lots']:.4f} → Rounded: **{result['lots']} lots**")

        with c2:
            st.markdown("**Costs & Exposure**")
            st.write(f"• Total Spread Cost: {result['currency']} {result['total_spread_cost']:,.2f}")
            st.write(f"• Total Commission: {result['currency']} {result['total_commission']:,.2f}")
            st.write(f"• Est. Swap ({result['holding_days']} days): {result['currency']} {result['total_swap']:,.2f}")
            st.write(f"• Margin % of Account: {result['margin_pct_of_account']:.2f}%")
            st.write(f"• Leverage: {result['leverage']:.0f}:1")

        # R:R section
        if result["target_price"]:
            st.divider()
            st.subheader("🎯 Risk : Reward Analysis")

            rr1, rr2, rr3, rr4 = st.columns(4)
            with rr1:
                st.metric("R:R Ratio", result["rr_text"])
            with rr2:
                st.metric("Reward Amount", f"{result['currency']} {result['reward_amount']:,.2f}")
            with rr3:
                st.metric("Breakeven Win Rate", f"{result['breakeven_winrate']:.1f}%")
            with rr4:
                st.metric("Target Price", f"{result['target_price']:,.2f}")

            # Visual R:R bar
            risk_width = 100 / (1 + result["rr_ratio"]) if result["rr_ratio"] else 50
            reward_width = 100 - risk_width

            st.markdown(f"""
            <div style="display: flex; height: 30px; border-radius: 5px; overflow: hidden; margin-top: 10px;">
                <div style="width: {risk_width}%; background-color: #dc3545; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">RISK</div>
                <div style="width: {reward_width}%; background-color: #28a745; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">REWARD</div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.divider()
st.caption("""
**Disclaimer:** This calculator provides estimates only. Always verify contract specifications, margin requirements, 
and swap rates with your broker before trading. CFDs are leveraged products and carry significant risk of loss.
""")
