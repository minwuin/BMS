import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import pandas as pd
import sys
import os
from datetime import datetime

# 1. 상위 폴더의 db_handler를 불러오기 위한 설정
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import db_handler

# 2. 페이지 설정
st.set_page_config(page_title="2층 강의실 실시간 좌석도", layout="wide")

# 이미지 경로 설정 (로비 이미지와 동일한 폴더 기준)
IMG_CLASSROOM = r"miniproject/allaboutus/pages/classroom.png"

# 세션 상태 초기화 (정보 표시용)
if "selected_desk_id" not in st.session_state: st.session_state.selected_desk_id = None
if "info_type" not in st.session_state: st.session_state.info_type = None

# --- [A] 상단 제목 및 뒤로가기 ---
col_title, col_back = st.columns([8, 2])
with col_title:
    st.title("🖥️ 2층 강의실 실시간 좌석도")
with col_back:
    if st.button("⬅️ 로비로 돌아가기", use_container_width=True):
        st.switch_page("pages/Floor2.py")

# --- [B] 하단 좌우 분할 (7:3 비율) ---
main_col, info_col = st.columns([7, 3])

with main_col:
    # [강의실 좌석 클릭 감지] - 팀원의 좌표 로직을 그대로 사용하기 위해 coordinates 사용
    coords = streamlit_image_coordinates(IMG_CLASSROOM, key="classroom_map_final", use_column_width=True)
    
    if coords:
        cx, cy = coords["x"], coords["y"]
        
        # --- [구역 체크 로직: 기존 코드 유지] ---
        # 1. 강사님 구역 (좌측 상단)
        if 3 <= cx <= 162 and 60 <= cy <= 125:
            if st.session_state.info_type != "teacher":
                st.session_state.info_type = "teacher"
                st.session_state.selected_desk_id = None
                st.rerun()
        
        # 2. 간식 구역 (중앙 하단)
        elif 400 <= cx <= 490 and 500 <= cy <= 850:
            if st.session_state.info_type != "snack":
                st.session_state.info_type = "snack"
                st.session_state.selected_desk_id = None
                st.rerun()
        
        # 3. 그 외 구역 (책상 검사)
        else:
            # 책상 배치 기준값
            start_x, start_y = 13, 170
            desk_w, desk_h = 74, 48
            gap_x, gap_y = 77, 82
            aisle_w = 95

            try:
                # db_handler를 통해 데이터 가져오기
                df_desks = db_handler.get_classroom_desks()

                found_id = None
                for _, d in df_desks.iterrows():
                    row, col = d['row_idx'], d['col_idx']
                    sx = start_x + (col * gap_x) + (aisle_w if col >= 5 else 0)
                    sy = start_y + (row * gap_y)
                    
                    if sx <= cx <= sx + desk_w and sy <= cy <= sy + desk_h:
                        found_id = str(d['desk_id'])
                        break
                
                if found_id and st.session_state.selected_desk_id != found_id:
                    st.session_state.selected_desk_id = found_id
                    st.session_state.info_type = "student"
                    st.rerun()
            except Exception as e:
                st.error(f"데이터 조회 오류: {e}")

# --- [C] 오른쪽 정보 표시 영역 ---
with info_col:
    st.subheader("ℹ️ 상세 정보")
    current_info = st.session_state.get("info_type")

    # 1. 강사님 정보
    if current_info == "teacher":
        st.success("👨‍🏫 강사님 정보")
        with st.container(border=True):
            st.write("### **김기석 강사**")
            st.write("**이메일:** instructor@example.com")
            st.divider()
            st.caption("질문 사항은 슬랙이나 메일로 부탁드립니다.")

    # 2. 간식 정보 표시
    elif current_info == "snack":
        st.success("🍪 실시간 간식 재고")
        try:
            # db_handler의 통합 함수 호출
            df_snack = db_handler.get_snack_inventory_status()
            st.dataframe(df_snack, use_container_width=True, hide_index=True)
        except:
            st.error("간식 데이터를 불러올 수 없습니다.")

    # 3. 좌석 정보 표시
    elif current_info == "student" and st.session_state.get("selected_desk_id"):
        try:
            # db_handler의 학생 정보 조회 함수 호출
            df_student = db_handler.get_student_info_by_desk(st.session_state.selected_desk_id)

            if not df_student.empty:
                s = df_student.iloc[0]
                st.success(f"**좌석 {st.session_state.selected_desk_id}**")
                with st.container(border=True):
                    st.write(f"### 👤 {s['name']}")
                    st.write(f"**📞 전화:** {s['phone']}")
                    st.write(f"**🎓 전공:** {s['major']}")
            else:
                st.warning("배정되지 않은 좌석입니다.")
        except:
            st.error("학생 정보 조회 실패")
    
    else:
        st.info("지도에서 좌석이나 구역을 클릭해 주세요.")