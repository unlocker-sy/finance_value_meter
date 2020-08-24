import json
import dart_fss as dart


# '''
# API, 사용법에 대한 내용은 아래 url을 참고
# https://pypi.org/project/dart-fss/
# 패키지 설치는 아래 명령으로
# pip install dart-fss
# '''
class CorpData():
    def __init__(self, str_name, str_code):
        print("__init__")
        self.str_name = str_name
        self.str_code = str_code

    def get_corp_list(self):
        print("get_corp_list")
        self.corp_list = dart.get_corp_list()
    
    def find_by_corp_name_from_list(self, name):
        print("find_by_corp_name_from_list")
        return self.corp_list.find_by_corp_name(name, exactly=True)[0]

    def find_by_stock_code(self, str_code):
        print("find_by_stock_code")
        self.corp = self.corp_list.find_by_stock_code(str_code)

    def extract_finance_sheet(self, str_name, str_code, is_fs_list):
        print('extract_finance_sheet')
        # 회사 검색
        if is_fs_list == True:
            print("get multi fs from corp_list")
            self.corp = self.find_by_corp_name_from_list(str_name)
        else:
            print("get single fs from corp")
            self.corp = self.find_by_stock_code(str_code)
        
        # 2017년부터 연간 연결재무제표 불러오기
        # TODO: date 표기법 통일 및 전달인자 처리 필요
        self.fs = self.corp.extract_fs(bgn_de='20170101')
        return self.fs

class FinanceSheet():
    def __init__(self, str_name, str_code):
        print("__init__")
        self.str_name = str_name
        self.str_code = str_code
        self.corp_data = CorpData(str_name, str_code)

        with open('info.json') as json_file:
            self.json_data = json.load(json_file)

        self.dart_key = self.json_data["dart_key"]

        # Open DART API KEY 설정
        dart.set_api_key(api_key=self.dart_key)

    def get_corp_list(self):
        return self.corp_data.get_corp_list()

    def get_finance_sheet_excel(self):
        print("get_finance_sheet_excel")
        self.fs = self.corp_data.extract_finance_sheet(self.str_name, self.str_code, True)
        
        # 재무제표 검색 결과를 엑셀파일로 저장 ( 기본저장위치: 실행폴더/fsdata )
        self.fs.save()

    def get_finance_sheet_list_dict(self):
        print("get_finance_sheet_list_dict")
        self.fs = self.corp_data.extract_finance_sheet(self.str_name, self.str_code, True)

    def get_single_finance_sheet_dict(self):
        print("get_finance_sheet_dict")
        self.fs = self.corp_data.extract_finance_sheet(self.str_name, self.str_code, True)

    def update_finance_sheet_all(self, name):
        print("update_finance_sheet_all")
        self.update_balance_sheet()
        self.update_income_statement()
        self.update_consolidated_income_statement()
        self.update_cash_flow()

    def update_balance_sheet(self):
        print("get_balance_sheet")
        # 연결재무상태표(Balance Sheet)
        self.df_bs = self.fs['bs'] # 또는 df = fs[0] 또는 df = fs.show('bs')
        # 연결재무상태표 추출에 사용된 Label 정보
        self.labels_bs = self.fs.labels['bs']
        print("===== 연결 재무 상태표 =====")
        print(type(self.df_bs))
        print(self.df_bs)
        print(self.labels_bs)

    def update_income_statement(self):
        # 연결손익계산서(Incom Statement)
        self.df_is = self.fs['is'] # 또는 df = fs[1] 또는 df = fs.show('is')
        # 연결손익계산서 추출에 사용된 Label 정보
        self.labels_is = self.fs.labels['is']
        print("===== 연결 손익 계산서 =====")
        print(type(self.df_is))
        print(self.df_is)
        print(self.labels_is)
    
    def update_consolidated_income_statement(self):
        # 연결포괄손익계산서(Consolidated Income Statement)
        self.df_ci = self.fs['cis'] # 또는 df = fs[2] 또는 df = fs.show('cis')
        # 연결포괄손익계산서 추출에 사용된 Label 정보
        self.labels_ci = self.fs.labels['cis']
        print("===== 연결 포괄 손익 계산서 =====")
        print(type(self.df_ci))
        print(self.df_ci)
        print(self.labels_ci)
    
    def update_cash_flow(self):
        # 현금흐름표(Cash Flow)
        self.df_cf = self.fs['cf'] # 또는 df = fs[3] 또는 df = fs.show('cf')
        # 현금흐름표 추출에 사용된 Label 정보
        self.labels_cf = self.fs.labels['cf']
        print("===== 현금 흐름표 =====")
        print(type(self.df_cf))
        print(self.df_cf)
        print(self.labels_cf)

    

if __name__ == "__main__":
    # print("check finance data")
    str_name = '삼성전자'
    str_code = '005930'

    finance_data = FinanceSheet(str_name, str_code)
    finance_data.get_corp_list()
    # 단일 종목만 가져오지 못한다.. 무조건 CorpList를 가져온뒤에 CorpList에서 가져오도록 되어있다.
    # finance_data.get_finance_sheet_dict()
    finance_data.get_finance_sheet_excel()

    # finance_data.get_single_finance_sheet_dict()

    # finance_data.update_finance_sheet_all('삼성전자')
    # finance_data.update_consolidated_income_statement()
    