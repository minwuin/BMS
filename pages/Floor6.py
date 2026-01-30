import streamlit as st
import base64
import os
import sys
import db_handler
from st_click_detector import click_detector 
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import db_handler 

from st_click_detector import click_detector 

st.set_page_config(layout="wide", page_title="7층 프로젝트룸")

IMG_PATH_6F = r"miniproject/allaboutus/pages/6floor.png"

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

st.title("🏛️ 대구 스마트시티 7층 관리 페이지")
st.markdown('<div id="map-section"></div>', unsafe_allow_html=True) 
st.write("지도에서 구역을 클릭하여 상세 정보를 확인하고 예약을 진행하세요.")

rooms_data = {
    "프로젝트룸 1": [15.86, 0.62, 32.97, 17.36],
    "프로젝트룸 2": [33.99, 0.69, 51.10, 17.43],
    "프로젝트룸 3": [3.11, 41.31, 19.91, 55.68],
    "프로젝트룸 4": [27.06, 35.06, 36.79, 61.17],
    "프로젝트룸 5": [58.92, 21.73, 75.37, 34.64],
    "프로젝트룸 6": [59.06, 37.70, 75.41, 50.75],
    "프로젝트룸 7": [79.85, 21.80, 96.25, 34.64],
    "프로젝트룸 8": [80.21, 37.91, 96.61, 50.89],
    "화장실": [37.37, 84.77, 56.39, 99.07]
}

col_left, col_right = st.columns([7, 3])

with col_left:
    img_b64 = get_image_base64(IMG_PATH_6F)
    if img_b64:
        content = f"""<div style="position: relative; display: inline-block;">
                        <img src="data:image/png;base64,{img_b64}" style="width: 100%; height: auto; border-radius: 15px; border: 1px solid #ddd;">"""
        for name, b in rooms_data.items():
            content += f"""<a id="{name}" href="#map-section" style="position: absolute; left: {b[0]}%; top: {b[1]}%; width: {b[2]-b[0]}%; height: {b[3]-b[1]}%; background-color: rgba(255, 255, 255, 0); z-index: 10;"></a>"""
        content += "</div>"
        clicked_room = click_detector(content)
    else:
        st.warning("이미지 파일을 찾을 수 없습니다.")
        clicked_room = ""

with col_right:
    if clicked_room and "프로젝트룸" in clicked_room:
        st.subheader(f"📍 {clicked_room}")
        room_num = int(clicked_room.split()[-1])
        
        # 1. 예약 목록 출력 (항상 노출)
        st.markdown("**📅 현재 예약 현황**")
        df_res = db_handler.get_room_reservations(room_num)
        if not df_res.empty:
            disp_df = df_res.copy()
            disp_df['start_time'] = disp_df['start_time'].dt.strftime('%H:%M')
            disp_df['end_time'] = disp_df['end_time'].dt.strftime('%H:%M')
            st.dataframe(disp_df[['student_name', 'start_time', 'end_time', 'purpose']], use_container_width=True, hide_index=True)
        else:
            st.info("등록된 예약이 없습니다.")

        # 2. [변경] 예약 신청 구역 (Expander)
        with st.expander("📝 새 예약 신청하기"):
    # form을 빼고 직접 위젯 배치 (테두리가 하나 사라짐)
            s_name = st.text_input("학생 이름", key="new_s_name")
            s_time = st.time_input("시작 시간", value=datetime.now(), key="new_s_time")
            e_time = st.time_input("종료 시간", value=datetime.now() + timedelta(hours=1), key="new_e_time")
            p_text = st.text_input("사용 목적", key="new_p_text")
            s_pw = st.text_input("취소 비밀번호(숫자 4자리)", type="password", key="new_s_pw")
    
            if st.button("예약 확정하기"):
                if s_name and s_pw:
                    today = datetime.now().date()
                    start_dt = datetime.combine(today, s_time)
                    end_dt = datetime.combine(today, e_time)
                    success, msg = db_handler.add_reservation(room_num, s_name, start_dt, end_dt, p_text, s_pw)
                    if success: 
                        st.success(msg)
                        st.rerun()
                    else: 
                        st.error(f"실패: {msg}")
                else:
                    st.warning("이름과 비밀번호를 입력해주세요.")

        # 3. 예약 취소 구역 (Expander)
        if not df_res.empty:
            with st.expander("🗑️ 예약 취소하기"):
                cancel_opts = {f"ID:{r['res_id']} - {r['student_name']}": r['res_id'] for _, r in df_res.iterrows()}
                target_key = st.selectbox("취소할 예약 선택", options=list(cancel_opts.keys()))
                c_pw = st.text_input("취소 비밀번호 입력", type="password", key="c_pw_input")
                
                if st.button("예약 취소 실행"):
                    success, msg = db_handler.delete_room_reservation(cancel_opts[target_key], c_pw)
                    if success: st.success(msg); st.rerun()
                    else: st.error(msg)

    elif clicked_room == "화장실":
        st.subheader("🚽 화장실 예약 시스템")
        selected_gender = st.radio("성별 선택", ["남", "여"], horizontal=True)
        
        st.markdown(f"**📅 오늘 {selected_gender}자 예약 현황**")
        df_toilet = db_handler.get_toilet_reservations(selected_gender)
        if not df_toilet.empty:
            disp_toilet = df_toilet.copy()
            disp_toilet['start_time'] = disp_toilet['start_time'].dt.strftime('%H:%M')
            disp_toilet['end_time'] = disp_toilet['end_time'].dt.strftime('%H:%M')
            st.dataframe(disp_toilet[['student_name', 'start_time', 'end_time']], use_container_width=True, hide_index=True)
        else:
            st.info("등록된 예약이 없습니다.")

        # [수정] st.form을 제거하여 이중 테두리를 없애고 깔끔하게 구성
        with st.expander("📝 화장실 사용 신청하기"):
            t_name = st.text_input("학생 이름", key="t_name_input")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                t_start = st.time_input("시작 시간", value=datetime.now(), key="t_start_input")
            with col_t2:
                t_end = st.time_input("종료 시간", value=datetime.now() + timedelta(minutes=15), key="t_end_input")
            
            t_pw = st.text_input("취소 비밀번호(숫자 4자리)", type="password", key="t_pw_input")
            
            # form_submit_button 대신 일반 button 사용
            if st.button("예약 확정하기", use_container_width=True):
                if t_name and t_pw:
                    today = datetime.now().date()
                    t_start_dt = datetime.combine(today, t_start)
                    t_end_dt = datetime.combine(today, t_end)
                    success, msg = db_handler.add_toilet_reservation(selected_gender, t_name, t_start_dt, t_end_dt, t_pw)
                    if success: 
                        st.success(msg)
                        st.rerun()
                    else: 
                        st.error(f"실패: {msg}")
                else:
                    st.warning("이름과 비밀번호를 입력해주세요.")

    # 화장실 예약 취소 구역 (Expander)
        if not df_toilet.empty:
            with st.expander("🗑️ 화장실 예약 취소하기"):
                t_cancel_opts = {f"ID:{r['res_id']} - {r['student_name']}": r['res_id'] for _, r in df_toilet.iterrows()}
                t_target_key = st.selectbox("취소할 예약 선택", options=list(t_cancel_opts.keys()), key="toilet_cancel")
                t_c_pw = st.text_input("비밀번호 입력", type="password", key="toilet_pw")
                if st.button("화장실 예약 취소 실행", use_container_width=True):
                    success, msg = db_handler.delete_toilet_reservation(t_cancel_opts[t_target_key], t_c_pw)
                    if success: st.success(msg); st.rerun()
                    else: st.error(msg)

    else:
        st.subheader("🗺️ 구역 선택")
        st.info("원하시는 구역을 지도에서 선택해 주세요!")
        st.write("지도의 **프로젝트룸**이나 **화장실** 영역을 클릭하면 해당 장소의 실시간 예약 현황을 확인하고 사용할 수 있습니다.")