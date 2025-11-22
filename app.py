import streamlit as st
import pandas as pd
import math

# 1. 페이지 설정
st.set_page_config(page_title="엘랑비탈 정기배송", page_icon="🏥", layout="wide")

# 2. 보안 설정
def check_password():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    def password_entered():
        if st.session_state["password"] == "I love VPMI":
            st.session_state.authenticated = True
            del st.session_state["password"]
        else:
            st.session_state.authenticated = False
    if not st.session_state.authenticated:
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.title("🔒 엘랑비탈 정기배송 v.2.3")
            st.text_input("비밀번호를 입력하세요:", type="password", on_change=password_entered, key="password")
        return False
    return True

if not check_password():
    st.stop()

# 3. 데이터 초기화
def init_session_state():
    if 'product_list' not in st.session_state:
        plist = []
        plist.extend(["시원한 것", "마시는 것", "커드 시원한 것", "EX"])
        plist.extend(["인삼 대사체", "표고버섯 대사체", "EDF", "장미꽃 대사체"])
        plist.extend(["애기똥풀 대사체", "인삼 사이다", "PAGI", "송이 대사체"])
        plist.extend(["PAGI 희석액", "Vitamin C", "SiO2"])
        plist.extend(["혼합 [E.R.P.V.P]", "혼합 [P.V.E]", "혼합 [P.P.E]"])
        plist.extend(["혼합 [Ex.P]", "혼합 [R.P]", "혼합 [Edf.P]", "혼합 [P.P]"])
        st.session_state.product_list = plist

    if 'patient_db' not in st.session_state:
        db = {}
        # -- 남양주 --
        items = [{"제품": "시원한 것", "용량": "280ml", "수량": 21}, {"제품": "커드 시원한 것", "용량": "280ml", "수량": 14}, {"제품": "EX", "용량": "280ml", "수량": 3}, {"제품": "인삼 대사체", "용량": "50ml", "수량": 7, "비고": "원액"}, {"제품": "표고버섯 대사체", "용량": "50ml", "수량": 7}]
        db["남양주 1"] = {"group": "남양주", "note": "⚠️ 신장 투석", "default": False, "items": items}

        items = [{"제품": "마시는 것", "용량": "280ml", "수량": 14}, {"제품": "시원한 것", "용량": "280ml", "수량": 14}, {"제품": "커드 시원한 것", "용량": "280ml", "수량": 14}, {"제품": "인삼 대사체", "용량": "50ml", "수량": 14}, {"제품": "EDF", "용량": "50ml", "수량": 7}, {"제품": "장미꽃 대사체", "용량": "50ml", "수량": 3}]
        db["남양주 2"] = {"group": "남양주", "note": "매주 발송", "default": True, "items": items}

        items = [{"제품": "시원한 것", "용량": "280ml", "수량": 14}, {"제품": "마시는 것", "용량": "280ml", "수량": 7}, {"제품": "커드 시원한 것", "용량": "280ml", "수량": 7}, {"제품": "인삼 대사체", "용량": "50ml", "수량": 7}, {"제품": "애기똥풀 대사체", "용량": "50ml", "수량": 7}]
        db["남양주 4"] = {"group": "남양주", "note": "매주 발송", "default": True, "items": items}

        # -- 유방암 --
        items = [{"제품": "혼합 [E.R.P.V.P]", "용량": "150ml", "수량": 14, "타입": "혼합"}, {"제품": "시원한 것", "용량": "280ml", "수량": 42}, {"제품": "마시는 것", "용량": "280ml", "수량": 14}, {"제품": "커드 시원한 것", "용량": "280ml", "수량": 14}]
        db["김동민 부인"] = {"group": "유방암", "note": "2주 간격", "default": True, "items": items}

        items = [{"제품": "인삼 사이다", "용량": "280ml", "수량": 14}, {"제품": "마시는 것", "용량": "280ml", "수량": 28}, {"제품": "시원한 것", "용량": "280ml", "수량": 28}, {"제품": "커드 시원한 것", "용량": "280ml", "수량": 14}, {"제품": "인삼 대사체", "용량": "50ml", "수량": 14}, {"제품": "송이 대사체", "용량": "50ml", "수량": 14}]
        db["김귀례"] = {"group": "유방암", "note": "2주 간격", "default": True, "items": items}

        items = [{"제품": "혼합 [P.V.E]", "용량": "150ml", "수량": 14, "타입": "혼합"}, {"제품": "혼합 [P.P.E]", "용량": "150ml", "수량": 14, "타입": "혼합"}, {"제품": "인삼 대사체", "용량": "50ml", "수량": 42}, {"제품": "시원한 것", "용량": "280ml", "수량": 42}, {"제품": "커드 시원한 것", "용량": "280ml", "수량": 28}]
        db["김성기"] = {"group": "유방암", "note": "2주 간격", "default": True, "items": items}

        items = [{"제품": "마시는 것", "용량": "280ml", "수량": 28}, {"제품": "시원한 것", "용량": "280ml", "수량": 28}, {"제품": "커드 시원한 것", "용량": "280ml", "수량": 28}, {"제품": "인삼 사이다", "용량": "280ml", "수량": 14}, {"제품": "PAGI", "용량": "50ml", "수량": 14}]
        db["최은찬"] = {"group": "유방암", "note": "2주 간격", "default": True, "items": items}

        items = [{"제품": "혼합 [Ex.P]", "용량": "150ml", "수량": 14, "타입": "혼합"}, {"제품": "혼합 [R.P]", "용량": "150ml", "수량": 14, "타입": "혼합"}, {"제품": "혼합 [Edf.P]", "용량": "150ml", "수량": 14, "타입": "혼합"}, {"제품": "혼합 [P.P]", "용량": "150ml", "수량": 14, "타입": "혼합"}, {"제품": "커드 시원한 것", "용량": "280ml", "수량": 14}, {"제품": "PAGI 희석액", "용량": "50ml", "수량": 14}]
        db["하혜숙"] = {"group": "유방암", "note": "2주 간격", "default": True, "items": items}

        st.session_state.patient_db = db

    if 'recipe_db' not in st.session_state:
        r_db = {}
        r_db["혼합 [E.R.P.V.P]"] = {"desc": "6배수 혼합/14병", "batch_size": 14, "materials": {"PAGI (50ml)": 12, "송이대사체 (50ml)": 6, "장미꽃 대사체 (50ml)": 6, "Vitamin C (3000mg)": 14, "SiO2 (1ml)": 14, "EX": 900}}
        r_db["혼합 [P.V.E]"] = {"desc": "1:1 개별 채움", "batch_size": 1, "materials": {"PAGI (50ml)": 1, "Vitamin C (3000mg)": 1, "EX": 100}}
        r_db["혼합 [P.P.E]"] = {"desc": "1:1 개별 채움", "batch_size": 1, "materials": {"송이대사체 (50ml)": 1, "인삼 대사체 (50ml)": 1, "EX": 50}}
        r_db["혼합 [Ex.P]"] = {"desc": "1:1 개별 채움", "batch_size": 1, "materials": {"PAGI (50ml)": 1, "EX": 100}}
        r_db["혼합 [R.P]"] = {"desc": "1:1 개별 채움", "batch_size": 1, "materials": {"장미꽃 대사체 (50ml)": 1, "PAGI (50ml)": 1, "인삼사이다": 50}}
        r_db["혼합 [Edf.P]"] = {"desc": "1:1 개별 채움", "batch_size": 1, "materials": {"EDF (50ml)": 1, "PAGI (50ml)": 1, "인삼사이다": 50}}
        r_db["혼합 [P.P]"] = {"desc": "1:1 개별 채움", "batch_size": 1, "materials": {"송이대사체 (50ml)": 1, "PAGI (50ml)": 1, "EX": 50}}
        st.session_state.recipe_db = r_db

init_session_state()

# ==========================================
# 🛠️ 사이드바
# ==========================================
with st.sidebar:
    st.header("📌 메뉴 선택")
    mode = st.radio("", ["📊 계산기 모드", "👤 신규 환자 등록", "🧪 신규 레시피 등록"])
    st.divider()
    st.info(f"User: faisos")

# ==========================================
# 1. 신규 환자 등록
# ==========================================
if mode == "👤 신규 환자 등록":
    st.title("👤 신규 환자 등록")
    st.markdown("---")
    c1, c2, c3 = st.columns([1, 1, 2])
    new_p_name = c1.text_input("환자 이름")
    new_p_group = c2.selectbox("그룹", ["남양주", "유방암", "기타"])
    new_p_note = c3.text_input("비고")
    
    if 'temp_items' not in st.session_state: st.session_state.temp_items = []
    
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        opts = ["(신규 입력)"] + sorted(st.session_state.product_list)
        sel = c1.selectbox("제품", opts)
        i_name = c1.text_input("신규명") if sel == "(신규 입력)" else sel
        i_vol = c2.selectbox("용량", ["280ml", "50ml", "150ml", "300ml"])
        i_qty = c3.number_input("수량", 1)
        if c4.button("담기 ➕"):
            if i_name:
                if i_name not in st.session_state.product_list: st.session_state.product_list.append(i_name)
                st.session_state.temp_items.append({"제품": i_name, "용량": i_vol, "수량": i_qty})
                st.rerun()

    if st.session_state.temp_items:
        st.write("🛒 담긴 목록")
        st.dataframe(pd.DataFrame(st.session_state.temp_items))
        if st.button("💾 저장", type="primary"):
            st.session_state.patient_db[new_p_name] = {"group": new_p_group, "note": new_p_note, "default": True, "items": st.session_state.temp_items}
            st.session_state.temp_items = []
            st.success(f"{new_p_name} 저장 완료!")

# ==========================================
# 2. 신규 레시피 등록
# ==========================================
elif mode == "🧪 신규 레시피 등록":
    st.title("🧪 신규 레시피 등록")
    st.markdown("---")
    
    all_prods = set()
    for i in st.session_state.patient_db.values():
        for x in i['items']:
            if "혼합" in str(x['제품']): all_prods.add(x['제품'])
    missing = list(all_prods - set(st.session_state.recipe_db.keys()))
    
    c1, c2 = st.columns([1, 1])
    if missing:
        c1.warning(f"🚨 미등록: {missing}")
        sel = c1.selectbox("제품", missing + ["(직접)"])
        r_name = c1.text_input("제품명", value="" if sel == "(직접)" else sel)
    else:
        r_name = c1.text_input("혼합 제품명")
    
    r_desc = c2.text_input("설명")
    r_batch = c2.number_input("배치 크기", 1)
    
    st.markdown("### 🥣 재료 담기")
    if 'temp_mats' not in st.session_state: st.session_state.temp_mats = {}
    
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        opts = ["(신규)"] + sorted(st.session_state.product_list)
        sel = c1.selectbox("재료", opts)
        m_name = c1.text_input("재료명") if sel == "(신규)" else sel
        m_qty = c2.text_input("수량/용량")
        if c3.button("추가 ➕"):
            if m_name and m_qty:
                if m_name not in st.session_state.product_list: st.session_state.product_list.append(m_name)
                try: val = float(m_qty)
                except: val = m_qty
                st.session_state.temp_mats[m_name] = val
                st.rerun()

    if st.session_state.temp_mats:
        st.table(pd.DataFrame(list(st.session_state.temp_mats.items()), columns=["재료", "양"]))
        if st.button("💾 저장", type="primary"):
            st.session_state.recipe_db[r_name] = {"desc": r_desc, "batch_size": r_batch, "materials": st.session_state.temp_mats}
            st.session_state.temp_mats = {}
            st.success("저장 완료!")

# ==========================================
# 3. 계산기 모드
# ==========================================
elif mode == "📊 계산기 모드":
    st.title("🏥 엘랑비탈 정기배송 v.2.3")
    col1, col2 = st.columns(2)
    with col1: target_date = st.date_input("발송일", value=pd.to_datetime("2025-11-25"))
    st.divider()

    db = st.session_state.patient_db
    sel_p = {}
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🚛 남양주 / 기타")
        for k, v in db.items():
            if v['group'] != "유방암":
                if st.checkbox(k, v['default'], help=v['note']): sel_p[k] = v['items']
    with c2:
        st.subheader("🚛 유방암")
        for k, v in db.items():
            if v['group'] == "유방암":
                if st.checkbox(k, v['default'], help=v['note']): sel_p[k] = v['items']
    
    st.divider()
    t1, t2, t3, t4 = st.tabs(["🏷️ 라벨", "🎁 장연구원", "🧪 한책임", "📊 원자재"])
    
    with t1:
        st.header("🖨️ 라벨 출력")
        st.info("💡 인쇄 시 '배경 그래픽' 옵션을 켜주세요.")
        if not sel_p: st.warning("환자를 선택하세요")
        else:
            cols = st.columns(2)
            for i, (name, items) in enumerate(sel_p.items()):
                with cols[i%2]:
                    with st.container(border=True):
                        st.markdown(f"### 🧊 {name}")
                        st.caption(f"📅 {target_date}")
                        st.markdown("---")
                        for x in items:
                            chk = "✅" if "혼합" in str(x['제품']) else "□"
                            # [수정] 비고 처리
                            note_text = f" ({x['비고']})" if "비고" in x else ""
                            # [핵심] 한 줄 표기: 제품명 + 수량 + (용량) + 비고
                            st.markdown(f"**{chk} {x['제품']}** {x['수량']}개 ({x['용량']}){note_text}")
                        st.markdown("---")
                        st.write("🏥 **엘랑비탈바이오**")

    with t2:
        st.header("🎁 장연구원 (개별 포장)")
        tot = {}
        for items in sel_p.values():
            for x in items:
                if "혼합" not in str(x['제품']):
                    k = f"{x['제품']} ({x['용량']})"
                    tot[k] = tot.get(k, 0) + x['수량']
        df = pd.DataFrame(list(tot.items()), columns=["제품", "수량"]).sort_values("수량", ascending=False)
        st.dataframe(df, use_container_width=True)

    with t3:
        st.header("🧪 한책임 (혼합 제조)")
        req = {}
        for items in sel_p.values():
            for x in items:
                if "혼합" in str(x['제품']): req[x['제품']] = req.get(x['제품'], 0) + x['수량']
        
        recipes = st.session_state.recipe_db
        total_mat = {}
        
        if not req: st.info("혼합 제품 없음")
        else:
            for p, q in req.items():
                if p in recipes:
                    with st.expander(f"📌 {p}", expanded=True):
                        c1, c2 = st.columns([1,2])
                        in_q = c1.number_input(f"{p} 수량", 0, value=q, key=f"{p}_{q}")
                        r = recipes[p]
                        c2.markdown(f"**{r['desc']}**")
                        ratio = in_q / r['batch_size'] if r['batch_size'] > 1 else in_q
                        for m, mq in r['materials'].items():
                            if isinstance(mq, (int, float)):
                                calc = mq * ratio
                                if "(50ml)" in m:
                                    vol = calc * 50
                                    c2.write(f"- {m}: **{calc:g}** (50*{calc:g}={vol:g} ml)")
                                elif "EX" in m or "사이다" in m:
                                    c2.write(f"- {m}: **{calc:g} ml**")
                                else:
                                    c2.write(f"- {m}: **{calc:g} 개**")
                                total_mat[m] = total_mat.get(m, 0) + calc
                            else: c2.write(f"- {m}: {mq}")

            st.divider()
            st.subheader("∑ 재료 총합")
            for k, v in sorted(total_mat.items(), key=lambda x: x[1], reverse=True):
                if "PAGI" in k and "희석액" not in k:
                    vol_ml = v * 50
                    st.info(f"💧 **{k}**: {v:g}개 (총 {vol_ml:,.0f} ml)")
                elif "사이다" in k:
                    bottles = v / 300
                    st.info(f"🥤 **{k}**: {v:,.0f} ml (약 {bottles:.1f}병)")
                elif "EX" in k:
                    st.info(f"🛢️ **{k}**: {v:,.0f} ml (약 {v/1000:.1f} L)")
                else:
                    st.success(f"📦 **{k}**: {v:g} 개")

    with t4:
        st.header("📊 원자재 예측")
        cnt = 0
        for items in sel_p.values():
            for x in items:
                if x['제품'] == "커드 시원한 것": cnt += x['수량']
        g = cnt * 280
        kg = round((g/6.5)/1000, 2)
        st.metric("커드 시원한 것", f"{cnt}개")
        st.info(f"💡 필요 우유: 약 {round(kg/9 * 16, 1)}통")
