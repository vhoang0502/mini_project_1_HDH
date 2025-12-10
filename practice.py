import csv
import os
import time
du_lieu=[]
try:
    with open("CSDL.csv" , mode="r" , encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            du_lieu.append(row)
except FileNotFoundError:
    print("File not found")

def print_data(du_lieu):
    headers=list(du_lieu[0].keys())
    #Lấy chiều rộng tối đa của từng cột
    col_width={}
    for header in headers:
        max_len=len(str(header))
        for row in du_lieu:
            max_len=max(max_len,len(str(row.get(header,''))))
        col_width[header]=max_len+2

    #In ra dữ liệu dạng bảng
    f_string = ""
    for header in headers:
        f_string+=f"{{:<{col_width[header]}}}"
    print(f_string.format(*headers))
    print("-"*(sum(col_width.values())-2))
    for row in du_lieu:
        row_string=[ str(tmp) for tmp in row.values() ]
        print(f_string.format(*row_string))
    print("-" * (sum(col_width.values()) - 2))
    print("[1].Find                 [2].Add")
    print("[3].Change               [4].Delete")
    print("[5].Exit")
    print("-" * (sum(col_width.values()) - 2))

#Tìm kiếm theo MSV
def Find(du_lieu):
    find_msv=input("Nhập mã sinh viên để tìm kiếm nhé: ")
    condition=0
    info=[]
    for row in du_lieu:
        msv=row.get("MSV","")
        if msv==find_msv:
            condition=1
            info.append(row)
            break
    if condition==0:
        print("----------------------------------")
        print("Không tìm thấy kết quả trùng khớp.")
        print("----------------------------------")
        print("Bạn có muốn tìm lại không?")
        print("[1].Có\n[2].Không")
        print("--------------------------")
        otp=int(input("Lựa chọn của bạn: "))
        if otp==1:
            os.system("cls")
            Find(du_lieu)
        else:
            print("Sẽ trở về trang chủ sau 2s.")
            time.sleep(2)
            os.system("cls")
            main()
    else:
        print("----------------------------------")
        print(f"MSV: {find_msv} có thông tin sau:")
        print(info)
        print("----------------------------------")
        print("Bạn có muốn tìm kiếm tiếp?")
        print("[1].Có    [2].Không")
        print("----------------------------------")
        otp=int(input("Nhập lựa chọn của bạn: "))
        if otp==1:
            os.system("cls")
            Find(du_lieu)
        else:
            print("Sẽ trở về trang chủ sau 2s.")
            time.sleep(2)
            os.system("cls")
            main()



#Xử lý lựa chọn
def xu_ly(n):
    if n==1:
        Find(du_lieu)
    # elif n==2:
    #   Add()
    # elif n==3:
    #   Change()
    # elif n==4:
    #   Delete()


#Hàm chính
def main():
    print_data(du_lieu)
    n=int(input("Nhập lựa chọn: "))
    os.system('cls')
    xu_ly(n)
main()
