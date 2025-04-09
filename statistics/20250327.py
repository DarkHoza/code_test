import numpy as np
import statistics
from collections import Counter
import os

def calculate_statistics(data):
    # 데이터가 비어있는지 확인
    if not data:
        return "데이터가 없습니다."
    
    # 기본 통계량 계산
    n = len(data)
    mean = float(sum(data) / n)
    
    # 분산 계산
    # 표본분산 (n-1로 나누기) - 일반적으로 통계학에서의 표준 분산
    if n > 1:  # n이 1인 경우 나눗셈 오류 방지
        sample_variance = float(sum((x - mean) ** 2 for x in data) / (n - 1))
        sample_std_dev = float(sample_variance ** 0.5)
    else:
        sample_variance = 0.0
        sample_std_dev = 0.0
    
    # 모집단분산 (n으로 나누기)
    population_variance = float(sum((x - mean) ** 2 for x in data) / n)
    population_std_dev = float(population_variance ** 0.5)
    
    # 범위 계산
    data_range = float(max(data) - min(data))
    
    # 정렬된 데이터
    sorted_data = sorted(data)
    
    # 중앙값(median) 계산
    if n % 2 == 0:  # 짝수 개수
        median = float((sorted_data[n//2 - 1] + sorted_data[n//2]) / 2)
    else:  # 홀수 개수
        median = float(sorted_data[n//2])
    
    # 최빈값(mode) 계산
    counter = Counter(data)
    most_common = counter.most_common()
    max_count = most_common[0][1]
    modes = [float(item) for item, count in most_common if count == max_count]
    
    # 모든 값이 동일한 빈도로 나타나는 경우 (모든 값이 최빈값)
    if len(modes) == len(set(data)):
        mode_result = "없음 (모든 값이 동일한 빈도)"
    else:
        mode_result = modes
    
    # IQR 계산 (위치 기반)
    # 위치 기반 1사분위수(Q1)와 3사분위수(Q3) 계산
    q1_position = (n + 1) * 0.25
    q3_position = (n + 1) * 0.75
    
    # 위치가 정수인 경우
    if q1_position.is_integer():
        q1 = float(sorted_data[int(q1_position) - 1])  # 0-indexed이므로 1을 빼줌
    else:
        # 위치가 정수가 아닌 경우 선형 보간법 사용
        lower_idx = int(q1_position)
        q1 = float(sorted_data[lower_idx - 1] + (q1_position - lower_idx) * (sorted_data[lower_idx] - sorted_data[lower_idx - 1]))
    
    if q3_position.is_integer():
        q3 = float(sorted_data[int(q3_position) - 1])  # 0-indexed이므로 1을 빼줌
    else:
        # 위치가 정수가 아닌 경우 선형 보간법 사용
        lower_idx = int(q3_position)
        q3 = float(sorted_data[lower_idx - 1] + (q3_position - lower_idx) * (sorted_data[lower_idx] - sorted_data[lower_idx - 1]))
    
    iqr = float(q3 - q1)
    
    return {
        "데이터 개수": n,
        "평균": mean,
        "중앙값": median,
        "최빈값": mode_result,
        "표본 분산 (n-1)": sample_variance,
        "표본 표준편차 (n-1)": sample_std_dev,
        "모집단 분산 (N)": population_variance,
        "모집단 표준편차 (N)": population_std_dev,
        "범위": data_range,
        "IQR": iqr,
        "Q1": q1,
        "Q3": q3
    }

def read_data_from_file(filename):
    """
    파일에서 데이터를 읽어오는 함수
    데이터는 쉼표(,)로 구분되어 있다고 가정
    """
    data = []
    
    try:
        # 현재 스크립트 파일과 같은 디렉토리에 있는 파일 경로 구성
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        
        with open(file_path, 'r') as file:
            content = file.read().strip()
            # 쉼표(,)로 구분된 데이터를 분리하고 공백 제거
            items = [item.strip() for item in content.split(',')]
            
            for item in items:
                if item:  # 빈 항목 무시
                    try:
                        data.append(float(item))
                    except ValueError:
                        print(f"경고: '{item}'은(는) 유효한 숫자가 아니어서 무시됩니다.")
    
    except FileNotFoundError:
        print(f"오류: '{filename}' 파일을 찾을 수 없습니다.")
        print(f"현재 작업 디렉토리: {os.getcwd()}")
        print("data.txt 파일이 현재 스크립트와 같은 디렉토리에 있는지 확인하세요.")
    except Exception as e:
        print(f"오류: 파일 읽기 중 문제가 발생했습니다. {str(e)}")
    
    return data

def main():
    print("data.txt 파일에서 데이터를 읽어옵니다...")
    
    data = read_data_from_file('data.txt')
    
    if not data:
        print("입력된 데이터가 없습니다.")
        return
    
    # 입력된 데이터 출력
    print("\n입력된 데이터:")
    # 정수인 경우 정수로, 실수인 경우 실수로 표시
    formatted_data = []
    for x in data:
        if x == int(x):  # 정수인 경우
            formatted_data.append(str(int(x)))
        else:  # 실수인 경우
            formatted_data.append(str(x))
    print(formatted_data)
    
    # 통계량 계산 및 출력
    stats = calculate_statistics(data)
    print("\n통계량:")
    for key, value in stats.items():
        if key == "데이터 개수":  # 데이터 개수는 정수로 표시
            print(f"{key}: {value}")
        elif key == "최빈값" and not isinstance(value, str):
            # 최빈값 형식 지정 (정수/실수 구분)
            modes_formatted = []
            for mode in value:
                if mode == int(mode):
                    modes_formatted.append(str(int(mode)))
                else:
                    modes_formatted.append(f"{mode:.4f}")
            print(f"{key}: [{', '.join(modes_formatted)}]")
        else:
            try:
                # 정수/실수 구분하여 출력
                if isinstance(value, (int, float)):
                    if value == int(value):  # 정수인 경우
                        print(f"{key}: {int(value)}")
                    else:  # 실수인 경우
                        print(f"{key}: {value:.4f}")
                else:
                    print(f"{key}: {value}")
            except (TypeError, ValueError):
                print(f"{key}: {value}")

if __name__ == "__main__":
    main()
