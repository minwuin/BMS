import streamlit as st
import base64
import os
import sys
from datetime import datetime
import re
import random

# 1. 상위 폴더의 db_handler를 불러오기 위한 설정
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import db_handler

from st_click_detector import click_detector 

# 2. 페이지 설정
st.set_page_config(layout="wide", page_title="2층 강의실 상세 현황")

# 이미지 경로 설정
IMG_CLASSROOM = r"miniproject/allaboutus/pages/classroom.png"

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


# 3. 상단 레이아웃 및 제목
col_t, col_b = st.columns([8, 2])
with col_t:
    st.title("🖥️ 강의실 관리 페이지")
    st.markdown('<div id="map-section"></div>', unsafe_allow_html=True) 
    st.write("지도에서 구역을 클릭하여 상세 정보를 확인하고 예약을 진행하세요.")
with col_b:
    # 로비로 돌아가기 버튼 (Streamlit 순정 기능 사용)
    if st.button("⬅️ 로비로 돌아가기", use_container_width=True):
        st.switch_page("pages/Floor2.py")

# 4. 강의실 구역 좌표 데이터 (보내주신 비율 좌표 적용)
# [좌측%, 상단%, 우측%, 하단%]
rooms_data = {
    # 책상 6~10
    "책상 6": [55.74, 30.43, 63.56, 37.42],
    "책상 7": [64.34, 30.49, 72.15, 37.43],
    "책상 8": [72.95, 30.49, 80.76, 37.22],
    "책상 9": [81.57, 30.49, 89.38, 37.22],
    "책상 10": [90.05, 30.28, 98.12, 37.43],
    # 책상 16~20
    "책상 16": [55.73, 45.00, 63.53, 51.73],
    "책상 17": [64.34, 44.79, 72.15, 51.51],
    "책상 18": [72.82, 44.79, 80.76, 51.73],
    "책상 19": [81.43, 44.79, 89.38, 51.73],
    "책상 20": [90.05, 44.58, 97.99, 51.51],
    # 책상 26~30
    "책상 26": [55.59, 59.08, 63.53, 66.02],
    "책상 27": [64.20, 59.29, 72.15, 66.02],
    "책상 28": [72.82, 59.08, 80.76, 65.81],
    "책상 29": [81.43, 58.87, 89.38, 65.81],
    "책상 30": [90.05, 59.08, 97.99, 66.02],
    # 1번~5번
    "책상 1": [2.04, 30.79, 9.19, 37.15],
    "책상 2": [10.77, 30.79, 17.99, 37.35],
    "책상 3": [19.44, 31.20, 26.66, 37.46],
    "책상 4": [27.85, 30.58, 35.33, 37.05],
    "책상 5": [36.51, 30.79, 43.87, 37.15],
    # 11번~15번
    "책상 11": [1.97, 45.15, 9.06, 51.62],
    "책상 12": [10.77, 45.15, 18.39, 51.52],
    "책상 13": [19.24, 45.05, 26.66, 51.52],
    "책상 14": [27.58, 45.15, 35.07, 51.52],
    "책상 15": [36.51, 45.05, 43.87, 51.31],
    # 21번~25번
    "책상 21": [1.97, 59.32, 9.46, 65.68],
    "책상 22": [10.64, 59.62, 17.99, 65.88],
    "책상 23": [19.24, 59.21, 26.53, 66.09],
    "책상 24": [27.98, 59.21, 35.07, 65.88],
    "책상 25": [36.58, 59.32, 43.74, 66.09],
    # 31번~35번
    "책상 31": [2.04, 73.48, 9.59, 80.25],
    "책상 32": [10.77, 73.68, 18.13, 80.46],
    "책상 33": [19.24, 73.48, 26.47, 80.05],
    "책상 34": [27.98, 73.89, 35.20, 80.25],
    "책상 35": [36.58, 73.48, 43.67, 80.46],
    # 기타 시설
    "강사님": [2.23, 11.90, 17.99, 19.91],
    "간식박스": [45.05, 87.95, 54.77, 99.13]
}

# 5. 메인 레이아웃 (7:3)
col_left, col_right = st.columns([7, 3])

with col_left:
    img_b64 = get_image_base64(IMG_CLASSROOM)
    if img_b64:
        click_nonce = random.randint(1, 10000)
        content = f"""<div style="position: relative; display: inline-block; width: 100%;">
                        <img src="data:image/png;base64,{img_b64}" style="width: 100%; height: auto; border-radius: 10px; border: 1px solid #ddd;">"""
        for name, b in rooms_data.items():
            target_id = f"{name}_{click_nonce}" if name == "강사님" else name
            content += f"""<a id="{name}" href="#map-section" style="
                            position: absolute; 
                            left: {b[0]}%; top: {b[1]}%; 
                            width: {b[2]-b[0]}%; height: {b[3]-b[1]}%; 
                            background-color: rgba(255, 255, 255, 0); 
                            z-index: 10;"></a>"""
        content += "</div>"
        clicked_id = click_detector(content)
    else:
        st.warning("강의실 이미지를 찾을 수 없습니다.")
        clicked_id = ""

# 6. 우측 정보 표시 로직
with col_right:
    if clicked_id and "강사님" in clicked_id:
        st.subheader("👨‍🏫 강사님 정보")
        
        # 랜덤 재생 로직
        bgm_folder = "miniproject/allaboutus/bgm"
        voice_files = [f"{bgm_folder}/yes.mp3", f"{bgm_folder}/yes#2.mp3", f"{bgm_folder}/yes#3.mp3"]
        selected_voice = random.choice(voice_files)
        
        # 재생 시마다 브라우저 캐시를 깨기 위한 랜덤 nonce
        nonce = random.random()
        
        if os.path.exists(selected_voice):
            with open(selected_voice, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                # 렌더링 강제를 위해 고유한 ID(nonce)를 div에 부여
                audio_html = f"""<div style="display:none;" id="{nonce}">
                                    <audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>
                                 </div>"""
                st.markdown(audio_html, unsafe_allow_html=True)

        with st.container(border=True):
            st.write("### **김기석 강사**")
            st.write("**이메일:** instructor@example.com")
            st.divider()
            st.info("질문은 쉬는 시간이나 줌 채팅을 이용해 주세요.")

    # Lecture_Room.py의 col_right 내 '간식박스' 클릭 로직

    elif clicked_id == "간식박스":
        st.subheader("🍪 실시간 간식 현황")
        
        # 1. 현재 재고 현황 (기존 기능)
        try:
            df_inventory = db_handler.get_snack_inventory_status()
            st.dataframe(df_inventory, use_container_width=True, hide_index=True)
        except:
            st.error("재고 데이터를 불러올 수 없습니다.")

        st.divider()

        # 2. 간식 신청 Expander
        with st.expander("➕ 먹고 싶은 간식 신청하기", expanded=True):
            # A. 신청 현황 리스트 (Expander 최상단)
            st.markdown("**📅 최근 신청 내역**")
            df_apply = db_handler.get_snack_apply_list()
            if not df_apply.empty:
                st.dataframe(df_apply, use_container_width=True, hide_index=True)
            else:
                st.info("아직 신청된 내역이 없습니다.")
                
            st.divider()
            
            # B. 신청 입력란 (st.form 제거로 테두리 최소화)
            st.markdown("**📝 새로운 간식 요청**")
            app_name = st.text_input("본인 이름", key="snack_app_name")
            app_snack = st.text_input("간식 이름", key="snack_app_item")
            app_count = st.number_input("수량", min_value=1, max_value=20, value=1, key="snack_app_cnt")
            
            # 일반 버튼 사용하여 이중 테두리 제거
            if st.button("신청 데이터 전송", use_container_width=True):
                if app_name and app_snack:
                    success, msg = db_handler.add_snack_apply(app_name, app_snack, app_count)
                    if success:
                        st.success(msg)
                        st.rerun() # 목록 갱신을 위해 새로고침
                    else:
                        st.error(msg)
                else:
                    st.warning("이름과 간식명을 입력해주세요.")

    elif "책상" in clicked_id:
        st.subheader(f"📍 {clicked_id}")
        desk_num = re.sub(r'[^0-9]', '', clicked_id)
        try:
            df_student = db_handler.get_student_info_by_desk(desk_num)
            if not df_student.empty:
                s = df_student.iloc[0]
                st.success(f"**현재 이용자 정보**")
                with st.container(border=True):
                    st.write(f"### 👤 {s['name']}")
                    
                    # 학생 번호와 성별을 한 줄에 표시 (아이콘 활용)
                    col_sub1, col_sub2 = st.columns(2)
                    with col_sub1:
                        st.write(f"**🆔 학생 번호:** {s['student_id']}")
                    with col_sub2:
                        # gender 컬럼값('남' 또는 '여')에 따른 아이콘 처리
                        gender_icon = "👨" if s['gender'] == '남' else "👩"
                        st.write(f"**{gender_icon} 성별:** {s['gender']}")
                    
                    st.divider()
                    st.write(f"**📞 연락처:** {s['phone']}")
                    st.write(f"**📧 이메일:** {s['email']}")
                    st.write(f"**🎓 구분:** {s['major']}")
            else:
                st.warning("현재 배정되지 않은 빈 좌석입니다.")
        except Exception as e:
            st.error(f"학생 정보를 조회하는 중 오류가 발생했습니다: {e}")

    else:
        st.subheader("🗺️ 강의실 안내")
        st.info("좌석이나 시설을 클릭하여 상세 정보를 확인하세요.")
        st.write("- **책상**: 이용 중인 학생 정보 확인")
        st.write("- **강사님 구역**: 강사님 프로필 확인")
        st.write("- **간식박스**: 현재 남은 간식 재고 확인")