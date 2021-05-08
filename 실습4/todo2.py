# 전공평점은 전공과목들의 평균학점을 구하는 내용입니다
# 학점분류, 전체 평균학점, 전공과목 평균학점을 구하는 기능들이 포함되어야 합니다

class Grade():
    def __init__(self):
        self.total = 0              # 과목 숫자를 저장
        self.subject = dict()       # {과목이름1: 학점1, 과목이름2: 학점2 ...} 형태
        self.major_grades = []      # 전공 과목의 학점을 저장

    def input_major(self, grade):
        self.major_grades += [grade]

    def input_grade(self, name, grade): # ex) input_grade("논리학", classify_score(99))
        self.total += 1         # 과목을 새로 입력할 때마다 total 수 증가시킴
        self.subject[name] = grade

    def calc_total_avg(self):
        if self.total == 0:
            return 0.0
        total_sum = 0.0
        for score in self.subject.values():
            total_sum += score
        return round(total_sum / self.total, 2)

    def calc_major_avg(self):
        if len(self.major_grades) == 0:
            return 0.0
        total_sum = 0.0
        for score in self.major_grades:
            total_sum += score
        return round(total_sum / len(self.major_grades), 2)

    def classify_score(self, score):
        if score >= 95:
            return 4.5
        elif score >= 90:
            return 4.0
        elif score >= 85:
            return 3.5
        elif score >= 80:
            return 3.0
        elif score >= 75:
            return 2.5
        elif score >= 70:
            return 2.0
        elif score >= 65:
            return 1.5
        elif score >= 60:
            return 1.0
        elif score >= 55:
            return 0.5
        else:
            return 0.0

system = Grade()
state = int(input("0: 종료, 1: 점수 입력, 2: 전체 학점 평균 출력, 3: 전공 학점 평균 출력, 4: 학점 분류하기 "))
while(state != 0):
    if(state == 1):
        name = input("과목 명을 입력해주세요: ")
        is_major = int(input("전공 과목인가요? 전공이면 1을 입력해주세요: "))
        score = int(input("과목의 점수를 입력해주세요: "))

        if(is_major == 1):
            system.input_major(system.classify_score(score))

        system.input_grade(name, system.classify_score(score))

    elif(state == 2):
        print("전체 학점 평균: %.2f"%(system.calc_total_avg()))

    elif(state == 3):
        print("전공 학점 평균: %.2f"%(system.calc_major_avg()))

    elif(state == 4):
        name = input("학점 열람을 원하는 과목의 이름을 입력해주세요: ")
        if(name not in system.subject.keys()):
            print("입력하신 과목의 정보가 존재하지 않습니다.")
            state = int(input("0: 종료, 1: 점수 입력, 2: 전체 학점 평균 출력, 3: 전공 학점 평균 출력, 4: 학점 분류하기"))
            continue
        print("입력하신 과목의 학점은 %.2f입니다"%(system.subject[name]))

    state = int(input("0: 종료, 1: 점수 입력, 2: 전체 학점 평균 출력, 3: 전공 학점 평균 출력, 4: 학점 분류하기"))



class Grade2(Grade):
    def calc_total_avg(self):
        if self.total == 0:
            return 0.0
        total_sum = 0.0
        for score in self.subject.values():
            total_sum += score

        if 0 in self.subject.values():
            print("교수님 다음에도 뵈어요!^^")

        result = round(total_sum / self.total, 2)

        if result >= 4.0:
            print("Excellent")
        elif result >= 3.0:
            print("Good")
        elif result >= 2.0:
            print("Bad")
        else:
            print("...")

        return result

system = Grade2()
state = int(input("0: 종료, 1: 점수 입력, 2: 전체 학점 평균 출력, 3: 전공 학점 평균 출력, 4: 학점 분류하기 "))
while(state != 0):
    if(state == 1):
        name = input("과목 명을 입력해주세요: ")
        is_major = int(input("전공 과목인가요? 전공이면 1을 입력해주세요: "))
        score = int(input("과목의 점수를 입력해주세요: "))

        if(is_major == 1):
            system.input_major(system.classify_score(score))

        system.input_grade(name, system.classify_score(score))

    elif(state == 2):
        print("전체 학점 평균: %.2f"%(system.calc_total_avg()))

    elif(state == 3):
        print("전공 학점 평균: %.2f"%(system.calc_major_avg()))

    elif(state == 4):
        name = input("학점 열람을 원하는 과목의 이름을 입력해주세요: ")
        if(name not in system.subject.keys()):
            print("입력하신 과목의 정보가 존재하지 않습니다.")
            continue
        print("입력하신 과목의 학점은 %.2f입니다"%(system.subject[name]))

    state = int(input("0: 종료, 1: 점수 입력, 2: 전체 학점 평균 출력, 3: 전공 학점 평균 출력, 4: 학점 분류하기"))