import pymysql
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# DB 연결 정보 (기존 정보 유지)
DB_CONFIG = {
    "user": "root",
    "password": "4328",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "bootcamp_db",
    "charset": "utf8mb4"
}

engine = create_engine(f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

def get_student_id(student_name):
    query = "SELECT student_id FROM students WHERE name = %s"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (student_name,))
            result = cursor.fetchone()
            return result[0] if result else None
    finally:
        conn.close()

# --- 프로젝트룸 관련 ---
def get_room_reservations(room_number):
    query = """
    SELECT r.res_id, s.name as student_name, r.start_time, r.end_time, r.purpose
    FROM room_reservations r
    JOIN students s ON r.student_id = s.student_id
    WHERE r.room_number = %s
    ORDER BY r.start_time ASC
    """
    return pd.read_sql(query, con=engine, params=(room_number,))

def add_reservation(room_number, student_name, start_time, end_time, purpose, password):
    student_id = get_student_id(student_name)
    if not student_id: return False, f"'{student_name}' 학생을 찾을 수 없습니다."
    
    # password 컬럼 포함 저장
    query = "INSERT INTO room_reservations (room_number, student_id, start_time, end_time, purpose, password) VALUES (%s, %s, %s, %s, %s, %s)"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (room_number, student_id, start_time, end_time, purpose, password))
        conn.commit()
        return True, "예약이 완료되었습니다."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_room_reservation(res_id, password):
    # res_id와 password가 동시에 일치해야 삭제
    query = "DELETE FROM room_reservations WHERE res_id = %s AND password = %s"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (res_id, password))
            affected = cursor.rowcount
        conn.commit()
        return (True, "취소되었습니다.") if affected > 0 else (False, "비밀번호가 틀렸거나 이미 취소된 예약입니다.")
    finally:
        conn.close()

# --- 화장실 관련 ---
# --- 7층 화장실 관련 (테이블명: 7_toilet_reservation) ---

def get_toilet_reservations(gender):
    """7층 화장실 예약 현황을 조회합니다."""
    # FROM 절을 7_toilet_reservation으로 수정
    query = """
    SELECT tr.res_id, s.name as student_name, tr.start_time, tr.end_time
    FROM `7_toilet_reservation` tr
    JOIN students s ON tr.student_id = s.student_id
    WHERE tr.sex = %s
    ORDER BY tr.start_time ASC
    """
    return pd.read_sql(query, con=engine, params=(gender,))

def add_toilet_reservation(gender, student_name, start_time, end_time, password):
    """7층 화장실 예약을 추가합니다."""
    student_id = get_student_id(student_name)
    if not student_id: 
        return False, f"'{student_name}' 학생을 찾을 수 없습니다."
    
    # 7_toilet_reservation 테이블에 데이터 삽입
    query = "INSERT INTO `7_toilet_reservation` (sex, toilet_id, student_id, start_time, end_time, password) VALUES (%s, %s, %s, %s, %s, %s)"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (gender, 1, student_id, start_time, end_time, password))
        conn.commit()
        return True, "7층 화장실 예약이 완료되었습니다."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_toilet_reservation(res_id, password):
    """7층 화장실 예약을 취소합니다."""
    # 7_toilet_reservation 테이블에서 비밀번호 확인 후 삭제
    query = "DELETE FROM `7_toilet_reservation` WHERE res_id = %s AND password = %s"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (res_id, password))
            affected = cursor.rowcount
        conn.commit()
        return (True, "취소되었습니다.") if affected > 0 else (False, "비밀번호가 틀렸거나 이미 취소된 예약입니다.")
    finally:
        conn.close()

        # --- 2층 소파 관련 ---
def get_sofa_reservations(sofa_number):
    query = """
    SELECT sr.res_id, s.name as student_name, sr.start_time, sr.end_time
    FROM sofa_reservation sr
    JOIN students s ON sr.student_id = s.student_id
    WHERE sr.sofa_number = %s
    ORDER BY sr.start_time ASC
    """
    return pd.read_sql(query, con=engine, params=(sofa_number,))

def add_sofa_reservation(sofa_number, student_name, start_time, end_time, password):
    student_id = get_student_id(student_name)
    if not student_id: return False, f"'{student_name}' 학생을 찾을 수 없습니다."
    
    query = "INSERT INTO sofa_reservation (sofa_number, student_id, start_time, end_time, password) VALUES (%s, %s, %s, %s, %s)"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (sofa_number, student_id, start_time, end_time, password))
        conn.commit()
        return True, "소파 예약이 완료되었습니다."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_sofa_reservation(res_id, password):
    query = "DELETE FROM sofa_reservation WHERE res_id = %s AND password = %s"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (res_id, password))
            affected = cursor.rowcount
        conn.commit()
        return (True, "취소되었습니다.") if affected > 0 else (False, "비밀번호가 틀렸습니다.")
    finally:
        conn.close()

# --- 2층 화장실 관련 (테이블명: 2_toilet_reservation) ---
def get_2f_toilet_reservations(gender):
    query = """
    SELECT tr.res_id, s.name as student_name, tr.start_time, tr.end_time
    FROM `2_toilet_reservation` tr
    JOIN students s ON tr.student_id = s.student_id
    WHERE tr.sex = %s
    ORDER BY tr.start_time ASC
    """
    return pd.read_sql(query, con=engine, params=(gender,))

def add_2f_toilet_reservation(gender, student_name, start_time, end_time, password):
    student_id = get_student_id(student_name)
    if not student_id: return False, f"'{student_name}' 학생을 찾을 수 없습니다."
    
    query = "INSERT INTO `2_toilet_reservation` (sex, toilet_id, student_id, start_time, end_time, password) VALUES (%s, %s, %s, %s, %s, %s)"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (gender, 1, student_id, start_time, end_time, password))
        conn.commit()
        return True, "2층 화장실 예약이 완료되었습니다."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def delete_2f_toilet_reservation(res_id, password):
    """2층 화장실 예약을 취소합니다."""
    # 2_toilet_reservation 테이블에서 비밀번호 확인 후 삭제
    query = "DELETE FROM `2_toilet_reservation` WHERE res_id = %s AND password = %s"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (res_id, password))
            affected = cursor.rowcount
        conn.commit()
        return (True, "취소되었습니다.") if affected > 0 else (False, "비밀번호가 틀렸거나 이미 취소된 예약입니다.")
    finally:
        conn.close()


def get_snack_data():
    """간식 재고 데이터를 가져옵니다."""
    query = "SELECT snack_name, category, current_stock, price FROM snacks"
    return pd.read_sql(query, con=engine)

def get_seat_student_info(desk_id):
    """특정 좌석의 학생 정보를 조회합니다."""
    query = f"""
        SELECT s.name, s.phone, s.email, s.is_major 
        FROM desk d
        JOIN Students s ON d.student_id = s.student_id
        WHERE d.desk_id = %s
    """
    return pd.read_sql(query, con=engine, params=(desk_id,))

    # ==========================================
# 🎓 강의실(Lecture Room) 페이지 연동을 위한 전용 함수
# ==========================================

def get_classroom_desks():
    """
    모든 좌석의 ID와 행/열 좌표 정보를 가져옵니다.
    (팀원 코드의 책상 위치 판별 로직에서 사용됩니다.)
    """
    query = "SELECT desk_id, row_idx, col_idx FROM desk"
    return pd.read_sql(query, con=engine)

def get_snack_inventory_status():
    """
    실시간 간식 재고 및 상세 정보를 한글 컬럼명으로 가져옵니다.
    """
    query = """
        SELECT snack_name as '이름', 
               category as '종류', 
               current_stock as '재고', 
               price as '가격', 
               restock_date as '입고일' 
        FROM snacks
    """
    return pd.read_sql(query, con=engine)

# db_handler.py 내의 함수 수정
def get_student_info_by_desk(desk_id):
    # 컬럼명을 gender로 수정
    query = """
        SELECT s.student_id, s.name, s.gender, s.phone, s.email, 
               CASE WHEN s.is_major = 1 THEN '전공' ELSE '비전공' END as major
        FROM desk d
        JOIN students s ON d.student_id = s.student_id
        WHERE d.desk_id = %s
    """
    # [핵심] params에 (desk_id,) 처럼 콤마를 찍어야 '문자열'이 아닌 '튜플'로 인식되어 
    # "not all arguments converted..." 오류가 사라집니다.
    return pd.read_sql(query, con=engine, params=(desk_id,))

# db_handler.py에 유지할 함수들

def get_snack_apply_list():
    """간식 신청 현황 리스트를 가져옵니다."""
    query = """
        SELECT sa.snack_id, sa.snack_name as '간식명', sa.count as '수량', s.name as '신청자'
        FROM snacks_apply sa
        JOIN students s ON sa.apply_id = s.student_id
        ORDER BY sa.snack_id DESC
    """
    # 삭를 위해 snack_id를 쿼리에 추가했습니다.
    return pd.read_sql(query, con=engine)

def add_snack_apply(student_name, snack_name, count):
    """새로운 간식 신청을 데이터베이스에 저장합니다."""
    student_id = get_student_id(student_name) # 기존 함수 활용
    if not student_id:
        return False, f"'{student_name}' 학생을 찾을 수 없습니다."
    
    query = "INSERT INTO snacks_apply (snack_name, count, apply_id) VALUES (%s, %s, %s)"
    conn = get_db_connection() # 기존 커넥션 함수 활용
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (snack_name, count, student_id))
        conn.commit()
        return True, "간식 신청이 완료되었습니다!"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def delete_snack_apply(snack_id):
    """신청한 간식 내역을 삭제합니다."""
    query = "DELETE FROM snacks_apply WHERE snack_id = %s"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (snack_id,))
        conn.commit()
        return True, "신청 내역이 삭제되었습니다."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()        