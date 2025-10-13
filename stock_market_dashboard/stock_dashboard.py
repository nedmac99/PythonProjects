import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime


# --- DARK MODE TOGGLE ---
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")
if dark_mode:
    st.markdown(
        """
		<style>
		body, .main, .block-container { background-color: #222 !important; color: #eee !important; }
		.st-bb, .st-c6, .st-cg, .st-cj, .st-cq, .st-cr, .st-cs, .st-ct, .st-cu, .st-cv, .st-cw, .st-cx, .st-cy, .st-cz, .st-da, .st-db, .st-dc, .st-dd, .st-de, .st-df, .st-dg, .st-dh, .st-di, .st-dj, .st-dk, .st-dl, .st-dm, .st-dn, .st-do, .st-dp, .st-dq, .st-dr, .st-ds, .st-dt, .st-du, .st-dv, .st-dw, .st-dx, .st-dy, .st-dz, .st-e0, .st-e1, .st-e2, .st-e3, .st-e4, .st-e5, .st-e6, .st-e7, .st-e8, .st-e9, .st-ea, .st-eb, .st-ec, .st-ed, .st-ee, .st-ef, .st-eg, .st-eh, .st-ei, .st-ej, .st-ek, .st-el, .st-em, .st-en, .st-eo, .st-ep, .st-eq, .st-er, .st-es, .st-et, .st-eu, .st-ev, .st-ew, .st-ex, .st-ey, .st-ez, .st-f0, .st-f1, .st-f2, .st-f3, .st-f4, .st-f5, .st-f6, .st-f7, .st-f8, .st-f9, .st-fa, .st-fb, .st-fc, .st-fd, .st-fe, .st-ff, .st-fg, .st-fh, .st-fi, .st-fj, .st-fk, .st-fl, .st-fm, .st-fn, .st-fo, .st-fp, .st-fq, .st-fr, .st-fs, .st-ft, .st-fu, .st-fv, .st-fw, .st-fx, .st-fy, .st-fz, .st-g0, .st-g1, .st-g2, .st-g3, .st-g4, .st-g5, .st-g6, .st-g7, .st-g8, .st-g9, .st-ga, .st-gb, .st-gc, .st-gd, .st-ge, .st-gf, .st-gg, .st-gh, .st-gi, .st-gj, .st-gk, .st-gl, .st-gm, .st-gn, .st-go, .st-gp, .st-gq, .st-gr, .st-gs, .st-gt, .st-gu, .st-gv, .st-gw, .st-gx, .st-gy, .st-gz, .st-h0, .st-h1, .st-h2, .st-h3, .st-h4, .st-h5, .st-h6, .st-h7, .st-h8, .st-h9, .st-ha, .st-hb, .st-hc, .st-hd, .st-he, .st-hf, .st-hg, .st-hh, .st-hi, .st-hj, .st-hk, .st-hl, .st-hm, .st-hn, .st-ho, .st-hp, .st-hq, .st-hr, .st-hs, .st-ht, .st-hu, .st-hv, .st-hw, .st-hx, .st-hy, .st-hz, .st-i0, .st-i1, .st-i2, .st-i3, .st-i4, .st-i5, .st-i6, .st-i7, .st-i8, .st-i9, .st-ia, .st-ib, .st-ic, .st-id, .st-ie, .st-if, .st-ig, .st-ih, .st-ii, .st-ij, .st-ik, .st-il, .st-im, .st-in, .st-io, .st-ip, .st-iq, .st-ir, .st-is, .st-it, .st-iu, .st-iv, .st-iw, .st-ix, .st-iy, .st-iz, .st-j0, .st-j1, .st-j2, .st-j3, .st-j4, .st-j5, .st-j6, .st-j7, .st-j8, .st-j9, .st-ja, .st-jb, .st-jc, .st-jd, .st-je, .st-jf, .st-jg, .st-jh, .st-ji, .st-jj, .st-jk, .st-jl, .st-jm, .st-jn, .st-jo, .st-jp, .st-jq, .st-jr, .st-js, .st-jt, .st-ju, .st-jv, .st-jw, .st-jx, .st-jy, .st-jz, .st-k0, .st-k1, .st-k2, .st-k3, .st-k4, .st-k5, .st-k6, .st-k7, .st-k8, .st-k9, .st-ka, .st-kb, .st-kc, .st-kd, .st-ke, .st-kf, .st-kg, .st-kh, .st-ki, .st-kj, .st-kk, .st-kl, .st-km, .st-kn, .st-ko, .st-kp, .st-kq, .st-kr, .st-ks, .st-kt, .st-ku, .st-kv, .st-kw, .st-kx, .st-ky, .st-kz, .st-l0, .st-l1, .st-l2, .st-l3, .st-l4, .st-l5, .st-l6, .st-l7, .st-l8, .st-l9, .st-la, .st-lb, .st-lc, .st-ld, .st-le, .st-lf, .st-lg, .st-lh, .st-li, .st-lj, .st-lk, .st-ll, .st-lm, .st-ln, .st-lo, .st-lp, .st-lq, .st-lr, .st-ls, .st-lt, .st-lu, .st-lv, .st-lw, .st-lx, .st-ly, .st-lz, .st-m0, .st-m1, .st-m2, .st-m3, .st-m4, .st-m5, .st-m6, .st-m7, .st-m8, .st-m9, .st-ma, .st-mb, .st-mc, .st-md, .st-me, .st-mf, .st-mg, .st-mh, .st-mi, .st-mj, .st-mk, .st-ml, .st-mm, .st-mn, .st-mo, .st-mp, .st-mq, .st-mr, .st-ms, .st-mt, .st-mu, .st-mv, .st-mw, .st-mx, .st-my, .st-mz, .st-n0, .st-n1, .st-n2, .st-n3, .st-n4, .st-n5, .st-n6, .st-n7, .st-n8, .st-n9, .st-na, .st-nb, .st-nc, .st-nd, .st-ne, .st-nf, .st-ng, .st-nh, .st-ni, .st-nj, .st-nk, .st-nl, .st-nm, .st-nn, .st-no, .st-np, .st-nq, .st-nr, .st-ns, .st-nt, .st-nu, .st-nv, .st-nw, .st-nx, .st-ny, .st-nz, .st-o0, .st-o1, .st-o2, .st-o3, .st-o4, .st-o5, .st-o6, .st-o7, .st-o8, .st-o9, .st-oa, .st-ob, .st-oc, .st-od, .st-oe, .st-of, .st-og, .st-oh, .st-oi, .st-oj, .st-ok, .st-ol, .st-om, .st-on, .st-oo, .st-op, .st-oq, .st-or, .st-os, .st-ot, .st-ou, .st-ov, .st-ow, .st-ox, .st-oy, .st-oz, .st-p0, .st-p1, .st-p2, .st-p3, .st-p4, .st-p5, .st-p6, .st-p7, .st-p8, .st-p9, .st-pa, .st-pb, .st-pc, .st-pd, .st-pe, .st-pf, .st-pg, .st-ph, .st-pi, .st-pj, .st-pk, .st-pl, .st-pm, .st-pn, .st-po, .st-pp, .st-pq, .st-pr, .st-ps, .st-pt, .st-pu, .st-pv, .st-pw, .st-px, .st-py, .st-pz, .st-q0, .st-q1, .st-q2, .st-q3, .st-q4, .st-q5, .st-q6, .st-q7, .st-q8, .st-q9, .st-qa, .st-qb, .st-qc, .st-qd, .st-qe, .st-qf, .st-qg, .st-qh, .st-qi, .st-qj, .st-qk, .st-ql, .st-qm, .st-qn, .st-qo, .st-qp, .st-qq, .st-qr, .st-qs, .st-qt, .st-qu, .st-qv, .st-qw, .st-qx, .st-qy, .st-qz, .st-r0, .st-r1, .st-r2, .st-r3, .st-r4, .st-r5, .st-r6, .st-r7, .st-r8, .st-r9, .st-ra, .st-rb, .st-rc, .st-rd, .st-re, .st-rf, .st-rg, .st-rh, .st-ri, .st-rj, .st-rk, .st-rl, .st-rm, .st-rn, .st-ro, .st-rp, .st-rq, .st-rr, .st-rs, .st-rt, .st-ru, .st-rv, .st-rw, .st-rx, .st-ry, .st-rz, .st-s0, .st-s1, .st-s2, .st-s3, .st-s4, .st-s5, .st-s6, .st-s7, .st-s8, .st-s9, .st-sa, .st-sb, .st-sc, .st-sd, .st-se, .st-sf, .st-sg, .st-sh, .st-si, .st-sj, .st-sk, .st-sl, .st-sm, .st-sn, .st-so, .st-sp, .st-sq, .st-sr, .st-ss, .st-st, .st-su, .st-sv, .st-sw, .st-sx, .st-sy, .st-sz, .st-t0, .st-t1, .st-t2, .st-t3, .st-t4, .st-t5, .st-t6, .st-t7, .st-t8, .st-t9, .st-ta, .st-tb, .st-tc, .st-td, .st-te, .st-tf, .st-tg, .st-th, .st-ti, .st-tj, .st-tk, .st-tl, .st-tm, .st-tn, .st-to, .st-tp, .st-tq, .st-tr, .st-ts, .st-tt, .st-tu, .st-tv, .st-tw, .st-tx, .st-ty, .st-tz, .st-u0, .st-u1, .st-u2, .st-u3, .st-u4, .st-u5, .st-u6, .st-u7, .st-u8, .st-u9, .st-ua, .st-ub, .st-uc, .st-ud, .st-ue, .st-uf, .st-ug, .st-uh, .st-ui, .st-uj, .st-uk, .st-ul, .st-um, .st-un, .st-uo, .st-up, .st-uq, .st-ur, .st-us, .st-ut, .st-uu, .st-uv, .st-uw, .st-ux, .st-uy, .st-uz, .st-v0, .st-v1, .st-v2, .st-v3, .st-v4, .st-v5, .st-v6, .st-v7, .st-v8, .st-v9, .st-va, .st-vb, .st-vc, .st-vd, .st-ve, .st-vf, .st-vg, .st-vh, .st-vi, .st-vj, .st-vk, .st-vl, .st-vm, .st-vn, .st-vo, .st-vp, .st-vq, .st-vr, .st-vs, .st-vt, .st-vu, .st-vv, .st-vw, .st-vx, .st-vy, .st-vz, .st-w0, .st-w1, .st-w2, .st-w3, .st-w4, .st-w5, .st-w6, .st-w7, .st-w8, .st-w9, .st-wa, .st-wb, .st-wc, .st-wd, .st-we, .st-wf, .st-wg, .st-wh, .st-wi, .st-wj, .st-wk, .st-wl, .st-wm, .st-wn, .st-wo, .st-wp, .st-wq, .st-wr, .st-ws, .st-wt, .st-wu, .st-wv, .st-ww, .st-wx, .st-wy, .st-wz, .st-x0, .st-x1, .st-x2, .st-x3, .st-x4, .st-x5, .st-x6, .st-x7, .st-x8, .st-x9, .st-xa, .st-xb, .st-xc, .st-xd, .st-xe, .st-xf, .st-xg, .st-xh, .st-xi, .st-xj, .st-xk, .st-xl, .st-xm, .st-xn, .st-xo, .st-xp, .st-xq, .st-xr, .st-xs, .st-xt, .st-xu, .st-xv, .st-xw, .st-xx, .st-xy, .st-xz, .st-y0, .st-y1, .st-y2, .st-y3, .st-y4, .st-y5, .st-y6, .st-y7, .st-y8, .st-y9, .st-ya, .st-yb, .st-yc, .st-yd, .st-ye, .st-yf, .st-yg, .st-yh, .st-yi, .st-yj, .st-yk, .st-yl, .st-ym, .st-yn, .st-yo, .st-yp, .st-yq, .st-yr, .st-ys, .st-yt, .st-yu, .st-yv, .st-yw, .st-yx, .st-yy, .st-yz, .st-z0, .st-z1, .st-z2, .st-z3, .st-z4, .st-z5, .st-z6, .st-z7, .st-z8, .st-z9, .st-za, .st-zb, .st-zc, .st-zd, .st-ze, .st-zf, .st-zg, .st-zh, .st-zi, .st-zj, .st-zk, .st-zl, .st-zm, .st-zn, .st-zo, .st-zp, .st-zq, .st-zr, .st-zs, .st-zt, .st-zu, .st-zv, .st-zw, .st-zx, .st-zy, .st-zz { background-color: #222 !important; color: #eee !important; }
		</style>
	""",
        unsafe_allow_html=True,
    )

st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

st.title("📈 Stock Market Dashboard")


# --- Ticker Selection (Multiselect) ---
# Top 50 US stocks by market cap (as of 2025, static list) + popular cryptocurrencies
top_50_tickers = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "NVDA",
    "META",
    "BRK-B",
    "TSLA",
    "LLY",
    "V",
    "JPM",
    "UNH",
    "WMT",
    "MA",
    "XOM",
    "AVGO",
    "PG",
    "JNJ",
    "HD",
    "MRK",
    "COST",
    "ABBV",
    "ADBE",
    "PEP",
    "CVX",
    "KO",
    "BAC",
    "MCD",
    "TMO",
    "PFE",
    "ORCL",
    "DIS",
    "CSCO",
    "ABT",
    "ACN",
    "DHR",
    "LIN",
    "VZ",
    "NKE",
    "WFC",
    "INTC",
    "TXN",
    "MS",
    "AMGN",
    "NEE",
    "PM",
    "UNP",
    "BMY",
    "QCOM",
    "IBM",
]
crypto_tickers = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "BNB-USD",
    "XRP-USD",
    "ADA-USD",
    "DOGE-USD",
    "AVAX-USD",
    "DOT-USD",
    "LINK-USD",
    "MATIC-USD",
    "TRX-USD",
    "LTC-USD",
    "BCH-USD",
]
all_tickers = top_50_tickers + crypto_tickers
tickers = st.sidebar.multiselect(
    "Select Stock/Crypto Ticker(s)", options=all_tickers, default=["AAPL"]
)
if not tickers:
    tickers = ["AAPL"]


# --- Custom Date Range ---
st.sidebar.markdown("---")
st.sidebar.header("Chart Options")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))
if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")

# --- Compare Multiple Stocks (Overlay Chart) ---
if len(tickers) > 1:
    st.subheader("Compare Selected Stocks (Close Price)")
    normalize = st.checkbox("Normalize (Show % Change from Start)", value=False)
    ticker_closes = []
    ticker_names = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            close = (
                hist["Close"] if (not hist.empty and "Close" in hist.columns) else None
            )
            if close is not None and close.notna().sum() > 1:
                # Convert index to naive datetime (remove tz)
                close.index = (
                    close.index.tz_localize(None)
                    if close.index.tz is not None
                    else close.index
                )
                if normalize:
                    first_valid = close[close.first_valid_index()]
                    if first_valid != 0:
                        close = (close / first_valid) * 100
                    # else: leave as is
                ticker_closes.append(close)
                ticker_names.append(ticker)
        except Exception as e:
            st.write(f"Error fetching {ticker}: {e}")
            continue
    if ticker_closes:
        # Build a common date range covering all days in the selected range
        common_dates = pd.date_range(start=start_date, end=end_date, freq="D")
        aligned = [c.reindex(common_dates) for c in ticker_closes]
        compare_df = pd.concat(aligned, axis=1)
        compare_df.columns = ticker_names
        compare_df = compare_df.dropna(how="all")
    # Drop all-NaN rows
    compare_df = compare_df.dropna(how="all")
    if not compare_df.empty:
        y_label = "% of Start Price" if normalize else "Price"
        fig_compare = px.line(
            compare_df,
            x=compare_df.index,
            y=compare_df.columns,
            title="Stock/Crypto Comparison (Close Price)",
            labels={"value": y_label},
        )
        st.plotly_chart(fig_compare, use_container_width=True, key="compare-close")

# --- Individual Stock Details ---
for ticker in tickers:
    st.markdown(f"## {ticker.upper()}")
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        info = stock.info
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        continue

    # --- Key Stats ---
    st.subheader(f"Key Stats for {ticker.upper()}")
    # Use last close as fallback for current price
    last_close = (
        hist["Close"].iloc[-1] if not hist.empty and "Close" in hist.columns else "N/A"
    )
    current_price = info.get("currentPrice")
    if current_price is None or current_price == "N/A":
        current_price = last_close
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Price", f"${current_price}")
    col2.metric(
        "Open",
        f"${info.get('open', hist['Open'].iloc[-1] if not hist.empty and 'Open' in hist.columns else 'N/A')}",
    )
    col3.metric(
        "Day High",
        f"${info.get('dayHigh', hist['High'].iloc[-1] if not hist.empty and 'High' in hist.columns else 'N/A')}",
    )
    col4.metric(
        "Day Low",
        f"${info.get('dayLow', hist['Low'].iloc[-1] if not hist.empty and 'Low' in hist.columns else 'N/A')}",
    )

    # --- Price Chart ---
    st.subheader("Price Chart (Selected Range)")
    fig = px.line(
        hist, x=hist.index, y="Close", title=f"{ticker.upper()} Closing Price"
    )
    st.plotly_chart(fig, use_container_width=True, key=f"{ticker}-close")

    # --- Buy/Sell Recommendation (SMA Crossover) ---
    st.subheader(f"Buy/Sell Recommendations for {ticker.upper()} (SMA 10/30)")
    if not hist.empty and "Close" in hist.columns:
        df = hist.copy()
        df["SMA10"] = df["Close"].rolling(window=10).mean()
        df["SMA30"] = df["Close"].rolling(window=30).mean()
        df["Signal"] = 0
        df.loc[df["SMA10"] > df["SMA30"], "Signal"] = 1
        df.loc[df["SMA10"] < df["SMA30"], "Signal"] = -1
        df["Trade"] = df["Signal"].diff()
        buy_signals = df[df["Trade"] == 2]
        sell_signals = df[df["Trade"] == -2]
        # Use the most recent available data for the recommendation
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_signal = df["Signal"].iloc[-1] if not df.empty else 0
        last_price = df["Close"].iloc[-1] if not df.empty else None
        if last_signal == 1:
            recommendation = f"Buy (as of {now} at ${last_price:.2f})"
        elif last_signal == -1:
            recommendation = f"Sell (as of {now} at ${last_price:.2f})"
        else:
            recommendation = f"Hold (as of {now})"
        st.markdown(f"**Current Recommendation:** {recommendation}")
        st.markdown("**Recent Buy/Sell Signals:**")
        signals_table = pd.concat(
            [
                buy_signals[["Close"]].rename(columns={"Close": "Buy Price"}),
                sell_signals[["Close"]].rename(columns={"Close": "Sell Price"}),
            ],
            axis=1,
        )
        st.dataframe(signals_table.tail(5))

    # --- Candlestick Chart ---
    st.subheader("Candlestick Chart (Selected Range)")
    fig_candle = go.Figure(
        data=[
            go.Candlestick(
                x=hist.index,
                open=hist["Open"],
                high=hist["High"],
                low=hist["Low"],
                close=hist["Close"],
                name=ticker,
            )
        ]
    )
    fig_candle.update_layout(
        title=f"{ticker.upper()} Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
    )
    st.plotly_chart(fig_candle, use_container_width=True, key=f"{ticker}-candle")

    # --- Volume Chart ---
    st.subheader("Volume (Selected Range)")
    fig2 = px.bar(hist, x=hist.index, y="Volume", title=f"{ticker.upper()} Volume")
    st.plotly_chart(fig2, use_container_width=True, key=f"{ticker}-volume")

    # --- Company Description ---
    st.subheader("Company Description")
    st.write(info.get("longBusinessSummary", "No description available."))

    # --- Price Alerts ---
    st.sidebar.markdown("---")
    st.sidebar.header("Price Alerts")
    alert_price = st.sidebar.number_input(
        f"Alert if {ticker.upper()} crosses:",
        min_value=0.0,
        value=float(info.get("currentPrice", 0) or 0),
        key=f"alert-{ticker}",
    )
    if info.get("currentPrice"):
        if info["currentPrice"] >= alert_price > 0:
            st.warning(
                f"ALERT: {ticker.upper()} has reached or exceeded ${alert_price}!"
            )
