import streamlit as st
import base64
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import db_handler
from st_click_detector import click_detector 
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(layout="wide", page_title="2층 로비 현황")

IMG_PATH_2F = r"miniproject/allaboutus/pages/2floor.png"

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

st.title("🏛️ 대구 스마트시티 2층 통합 관리 페이지")
st.markdown('<div id="map-section"></div>', unsafe_allow_html=True) 
st.write("지도에서 구역을 클릭하여 상세 정보를 확인하고 예약을 진행하세요.")

# 2층 구역 좌표 데이터
rooms_data = {
    "강의실": [8.98, 0.65, 44.90, 32.35],
    "소파 1": [12.72, 51.96, 26.27, 61.32],
    "소파 2": [30.43, 51.96, 43.90, 61.58],
    "소파 3": [48.06, 51.96, 61.86, 61.71],
    "소파 4": [74.42, 51.84, 87.97, 61.58],
    "화장실": [55.46, 81.58, 74.17, 98.99]
}

col_left, col_right = st.columns([7, 3])

with col_left:
    img_b64 = get_image_base64(IMG_PATH_2F)
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
    if clicked_room == "강의실":
        st.subheader("👨‍🏫 강의실")
        st.info("강의실 상세 페이지로 이동합니다...")
        
        # [추천 방법] 다른 사람이 만든 파일명이 'Lecture_Room.py'라면
        # pages 폴더 안에 있는 파일 이름을 확장자 없이 입력합니다.
        st.switch_page("pages/Lecture_Room.py")

    elif "소파" in clicked_room:
        st.subheader(f"🛋️ {clicked_room}")
        sofa_num = int(clicked_room.split()[-1])
        
        st.markdown("**📅 현재 사용 현황**")
        df_sofa = db_handler.get_sofa_reservations(sofa_num)
        if not df_sofa.empty:
            disp_df = df_sofa.copy()
            disp_df['start_time'] = disp_df['start_time'].dt.strftime('%H:%M')
            disp_df['end_time'] = disp_df['end_time'].dt.strftime('%H:%M')
            st.dataframe(disp_df[['student_name', 'start_time', 'end_time']], use_container_width=True, hide_index=True)
        else:
            st.info("현재 이용 중인 학생이 없습니다.")

        with st.expander("📝 소파 사용 신청"):
            s_name = st.text_input("학생 이름", key="sofa_n")
            c1, c2 = st.columns(2)
            with c1: s_start = st.time_input("시작", value=datetime.now(), key="sofa_s")
            with c2: s_end = st.time_input("종료", value=datetime.now() + timedelta(minutes=30), key="sofa_e")
            s_pw = st.text_input("비밀번호(4자리)", type="password", key="sofa_p")
            if st.button("예약 확정", use_container_width=True):
                success, msg = db_handler.add_sofa_reservation(sofa_num, s_name, datetime.combine(datetime.now().date(), s_start), datetime.combine(datetime.now().date(), s_end), s_pw)
                if success: st.success(msg); st.rerun()
                else: st.error(msg)

        if not df_sofa.empty:
            with st.expander("🗑️ 소파 예약 취소하기"):
                s_cancel_opts = {f"ID:{r['res_id']} - {r['student_name']}": r['res_id'] for _, r in df_sofa.iterrows()}
                s_target_key = st.selectbox("취소할 예약 선택", options=list(s_cancel_opts.keys()), key="sofa_cancel_sel")
                s_c_pw = st.text_input("비밀번호 입력", type="password", key="sofa_pw_cancel")
                if st.button("소파 예약 취소 실행", use_container_width=True):
                    success, msg = db_handler.delete_sofa_reservation(s_cancel_opts[s_target_key], s_c_pw)
                    if success: st.success(msg); st.rerun()
                    else: st.error(msg)

    elif clicked_room == "화장실":
        st.subheader("🚽 2층 화장실 예약 시스템")
        selected_gender = st.radio("성별 선택", ["남", "여"], horizontal=True, key="2f_gender_radio")
        
        st.markdown(f"**📅 오늘 2층 {selected_gender}자 예약 현황**")
        # db_handler에서 2층 전용 조회 함수 호출
        df_toilet = db_handler.get_2f_toilet_reservations(selected_gender)
        
        if not df_toilet.empty:
            disp_toilet = df_toilet.copy()
            disp_toilet['start_time'] = disp_toilet['start_time'].dt.strftime('%H:%M')
            disp_toilet['end_time'] = disp_toilet['end_time'].dt.strftime('%H:%M')
            st.dataframe(disp_toilet[['student_name', 'start_time', 'end_time']], use_container_width=True, hide_index=True)
        else:
            st.info("등록된 예약이 없습니다.")

        # [UI 통일] st.form 없이 expander만 사용하여 테두리 제거
        with st.expander("📝 화장실 사용 신청하기"):
            t_name = st.text_input("학생 이름", key="2f_t_name_input")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                t_start = st.time_input("시작 시간", value=datetime.now(), key="2f_t_start_input")
            with col_t2:
                t_end = st.time_input("종료 시간", value=datetime.now() + timedelta(minutes=15), key="2f_t_end_input")
            
            t_pw = st.text_input("취소 비밀번호(숫자 4자리)", type="password", key="2f_t_pw_input")
            
            if st.button("예약 확정하기", use_container_width=True, key="2f_t_res_btn"):
                if t_name and t_pw:
                    today = datetime.now().date()
                    t_start_dt = datetime.combine(today, t_start)
                    t_end_dt = datetime.combine(today, t_end)
                    # db_handler에서 2층 전용 추가 함수 호출
                    success, msg = db_handler.add_2f_toilet_reservation(selected_gender, t_name, t_start_dt, t_end_dt, t_pw)
                    if success: 
                        st.success(msg)
                        st.rerun()
                    else: 
                        st.error(f"실패: {msg}")
                else:
                    st.warning("이름과 비밀번호를 입력해주세요.")

        # 화장실 예약 취소 구역
        if not df_toilet.empty:
            with st.expander("🗑️ 화장실 예약 취소하기"):
                t_cancel_opts = {f"ID:{r['res_id']} - {r['student_name']}": r['res_id'] for _, r in df_toilet.iterrows()}
                t_target_key = st.selectbox("취소할 예약 선택", options=list(t_cancel_opts.keys()), key="2f_toilet_cancel_sel")
                t_c_pw = st.text_input("비밀번호 입력", type="password", key="2f_toilet_pw_cancel")
                
                if st.button("화장실 예약 취소 실행", use_container_width=True, key="2f_t_cancel_btn"):
                    # 2층 테이블(2_toilet_reservation) 전용 삭제 함수 호출
                    # (db_handler에 delete_2f_toilet_reservation이 없다면 delete_toilet_reservation 함수를 테이블 인자값만 바꿔서 공용으로 쓰거나 추가해야 합니다)
                    success, msg = db_handler.delete_2f_toilet_reservation(t_cancel_opts[t_target_key], t_c_pw)
                    if success: 
                        st.success(msg)
                        st.rerun()
                    else: 
                        st.error(msg)
    else:
        st.subheader("🗺️ 구역 선택")
        st.info("원하시는 구역을 지도에서 선택해 주세요!")
        st.write("지도의 **강의실**이나 **화장실** 영역을 클릭하면 해당 장소의 상세 내용을 확인할 수 있습니다.")