import csv
import time
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.prompt import Prompt
from rich.panel import Panel

# du_lieu  : dữ liệu gốc
# table2   : chỉ để hiển thị

class DataManager:
    def __init__(self):
        self.du_lieu = []
        self.table = Table(title="Danh sách lớp học", show_lines=True)

    def load_data(self):
        self.du_lieu.clear()
        self.table.columns.clear()
        self.table.rows.clear()

        try:
            with open("CSDL.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.du_lieu.append(row)
        except FileNotFoundError:
            console.print("[bold red]Không tìm thấy file CSDL.csv[/bold red]")
            return

        if not self.du_lieu:
            return

        for header in self.du_lieu[0].keys():
            self.table.add_column(header, justify="center")

        for row in self.du_lieu:
            self.table.add_row(*row.values())

    # Lưu trữ vào CSV
    def save_to_csv(self):
        if not self.du_lieu:
            return

        with open("CSDL.csv", mode="w", encoding="utf-8", newline="") as file:
            fieldnames = self.du_lieu[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.du_lieu)

    # Tìm thông tin sinh viên theo mã sinh viên
    def find_by_msv(self, msv):
        return [row for row in self.du_lieu if row.get("MSV") == msv]

    # Tìm thông tin sinh viên theo tên sinh viên ( chữ cái cuối )
    def find_by_name(self, ten):
        ket_qua = []
        for row in self.du_lieu:
            ho_ten = row.get("Họ và Tên", "")
            if ho_ten:
                ten_cuoi = ho_ten.split()[-1]
                if ten_cuoi == ten:
                    ket_qua.append(row)
        return ket_qua

    # Kiểm tra xem msv có bị trùng hay không
    def is_duplicate_msv(self, msv):
        return any(sv.get("MSV") == msv for sv in self.du_lieu)

    # Thêm sinh viên mới vào dữ liệu
    def add_student(self, sv_moi):
        self.du_lieu.append(sv_moi)
        self.save_to_csv()

    # Tìm vị trí của mã sinh viên nhập vào
    def find_index_by_msv(self, msv):
        count=-1
        for row in self.du_lieu:
            count+=1
            if row.get("MSV") == msv:
                return count
        return -1

    # Thay đổi dữ liệu bằng mã sinh viên
    def update_by_msv(self, msv,sv_moi):
        index=self.find_index_by_msv(msv)
        if index == -1:
            return False
        self.du_lieu[index]=sv_moi
        self.save_to_csv()
        return True

    # Xóa dữ liệu bằng mã sinh viên
    def delete_by_msv(self, msv):
        index = self.find_index_by_msv(msv)
        if index == -1:
            return False
        del self.du_lieu[index]
        self.save_to_csv()
        return True

manager=DataManager()
console = Console()

# ================== Hiển thị bảng dữ liệu ==================
def print_data():
    if not manager.du_lieu:
        console.print("[yellow]Không có dữ liệu để hiển thị[/yellow]")
        return

    console.clear()
    console.print(
        Align.center(
            manager.table,
        )
    )

    console.print(
        Align.center(
            Panel(
                "[1] Find    [2] Add    [3] Change    [4] Delete",
                title="Chức năng",
                border_style="green",
                expand=False,
            )
        )
    )
    console.print(
        Align.center(
            Panel(
                "[M] Menu chính    [0] Thoát",
                border_style="green",
                expand=False,
            )
        )
    )

    choice = Prompt.ask(
        "Chọn một nút",
        choices=["1", "2", "3", "4", "5", "M", "0"],
    )

    if choice == "M":
        main_menu()
    elif choice == "1":
        find()
    elif choice == "0":
        exit()
    elif choice == "2":
        add()
    elif choice == "3":
        change()
    elif choice == "4":
        delete()
    else:
        console.print("[yellow]Chức năng đang phát triển[/yellow]")
        time.sleep(1)
        print_data()


def find_msv():
    console.clear()

    console.print(
        Align.center(
            Panel(
                "[bold cyan]Classroom Data Manager[/bold cyan]\n"
                "v0.1 by Team HDH",
                expand=False,
            )
        )
    )

    console.print(
        Align.center(
            "Tìm kiếm theo MSV",
            style="cyan",
        )
    )


    msv = Prompt.ask(
        "Nhập mã sinh viên muốn tìm kiếm"
    )

    ket_qua = Table(title=f"Kết quả tìm kiếm cho MSV: {msv}", show_lines=True)
    ket_qua_ds=manager.find_by_msv(msv)
    if ket_qua_ds:
        for header in manager.du_lieu[0].keys():
            ket_qua.add_column(header, justify="center", style="cyan")

        for row in ket_qua_ds:
            ket_qua.add_row(*row.values())

        console.clear()
        console.print(Align.center(ket_qua))
    else:
        console.print(f"[bold red]Không tìm thấy sinh viên có mã: {msv}[/bold red]")


    choice=Prompt.ask(
        "Bạn có muốn tiếp tục tìm kiếm? [Y/N]",
        choices=["Y", "N"],
        default="N",
    )
    if choice == "Y":
        find_msv()
    elif choice == "N":
        find()


def find_name():
    console.clear()
    # load_and_build_table()

    console.print(
        Align.center(
            Panel(
                "[bold cyan]Classroom Data Manager[/bold cyan]\n"
                "v0.1 by Team HDH",
                expand=False,
            )
        )
    )

    console.print(
        Align.center(
            "Tìm kiếm theo tên",
            style="cyan",
        )
    )

    name_temp=Prompt.ask(
        "Nhập tên sinh viên bạn muốn tìm"
    )

    ket_qua = Table(title=f"Kết quả tìm kiếm cho tên: {name_temp}", show_lines=True)

    ket_qua_ds = manager.find_by_name(name_temp)

    if ket_qua_ds:
        for header in manager.du_lieu[0].keys():
            ket_qua.add_column(header, justify="center", style="cyan")

        for row in ket_qua_ds:
            ket_qua.add_row(*row.values())

        console.clear()
        console.print(Align.center(ket_qua))
    else:
        console.print(f"[bold red]Không tìm thấy sinh viên có tên: {name_temp}[/bold red]")

    choice=Prompt.ask(
        "Bạn có muốn tiếp tục tìm kiếm? [Y/N]",
        choices=["Y", "N"],
        default="N",
    )

    if choice=="Y":
        find_name()
    elif choice=="N":
        find()

def find():
    console.clear()
    console.print(
        Align.center(
            "Chức năng tìm kiếm",
            style="bold cyan",
        )
    )
    menu_find="""
[1].Tìm kiếm theo tên
[2].Tìm kiếm theo MSV
    """
    menu_nav="""[R] Quay lại    [M] Menu chính    [0] Thoát"""
    console.print(
        Align.center(
            Panel(
                menu_find,
                title="Menu",
                expand=False,
            )
        )
    )
    console.print(
        Align.center(
            Panel(
                menu_nav,
                border_style="green",
                expand=False,
            )
        )
    )
    choice=Prompt.ask(
        "Nhập lựa chọn:",
        choices=["1","2","R","M","0"],
        default="0",

    )
    if choice=="0":
        exit()
    elif choice=="M":
        main_menu()
    elif choice=="R":
        print_data()
    elif choice=="1":
        find_name()
    elif choice=="2":
        find_msv()
    else:
        console.print("[yellow]Chức năng đang phát triển[/yellow]")
        time.sleep(1)
        print_data()

def add():
    console.clear()

    # load_and_build_table()

    console.print(
        Align.center(
            Panel(
                "[bold cyan]Classroom Data Manager[/bold cyan]\n"
                "v0.1 by Team HDH",
                expand=False,
            )
        )
    )

    console.print(
        Align.center(
            "Chức năng thêm sinh viên",
            style="cyan",
        )
    )

    while True:
        msv = Prompt.ask("Nhập Mã sinh viên")

        # Kiểm tra msv có tồn tại trong danh sách du_lieu hay chưa
        is_duplicate = manager.is_duplicate_msv(msv)

        if is_duplicate:
            console.print(f"[bold red]Lỗi: Mã sinh viên '{msv}' đã tồn tại! Vui lòng nhập mã khác.[/bold red]")
        elif msv == "":
            console.print("[bold yellow]Mã sinh viên không được để trống.[/bold yellow]")
        else:
            break

    ho_ten=Prompt.ask("Nhập họ và tên")
    sinh_nhat=Prompt.ask("Nhập ngày sinh")
    tp1=float(Prompt.ask("Nhập điểm tp1"))
    tp2=float(Prompt.ask("Nhập điểm tp2"))
    tmp=(tp1+tp2)/2
    diem_tong_ket= f"{tmp:.2f}"
    sv_moi={"MSV":msv,"Họ và Tên":ho_ten,"Ngày sinh":sinh_nhat,"Điểm TP1":str(tp1),"Điểm TP2":str(tp2),"Điểm tổng kết":str(diem_tong_ket)}

    manager.add_student(sv_moi)
    manager.load_data()
    console.print(f"[cyan]Đã thêm sinh viên {msv}.[/cyan]")
    console.print("Trở về trang chủ sau 1s...")
    time.sleep(1)

    console.clear()
    print_data()

def change():
    console.clear()
    console.print(
        Align.center(
            Panel(
                "[bold cyan]Classroom Data Manager[/bold cyan]\n"
                "v0.1 by Team HDH",
                expand=False,
            )
        )
    )
    console.print(
        Align.center(
            "Thay đổi thông tin sinh viên",
            style="cyan",
        )
    )
    msv=0
    while True:
        ask1 = Prompt.ask("Nhập mã sinh viên muốn thay đổi thông tin")
        msv=ask1
        if manager.is_duplicate_msv(ask1):
            msv=ask1
            break
        else:
            console.print(f"[bold red]Lỗi: Mã sinh viên '{msv}' không tồn tại! Vui lòng nhập mã khác.[/bold red]")

    ho_ten=Prompt.ask("Nhập họ và tên")
    sinh_nhat=Prompt.ask("Nhập ngày sinh")
    tp1=float(Prompt.ask("Nhập điểm tp1"))
    tp2=float(Prompt.ask("Nhập điểm tp2"))
    tmp=(tp1+tp2)/2
    diem_tong_ket= f"{tmp:.2f}"
    sv_moi={"MSV":msv,"Họ và Tên":ho_ten,"Ngày sinh":sinh_nhat,"Điểm TP1":str(tp1),"Điểm TP2":str(tp2),"Điểm tổng kết":str(diem_tong_ket)}

    manager.update_by_msv(msv,sv_moi)
    manager.load_data()
    console.print(f"[green]Đã thay đổi thông tin thành công.[/green]")
    console.print("Trở về trang chủ sau 1s...")
    time.sleep(1)

    console.clear()
    print_data()


def delete():
    console.clear()

    console.print(
        Align.center(
            Panel(
                "[bold cyan]Classroom Data Manager[/bold cyan]\n"
                "v0.1 by Team HDH",
                expand=False,
            )
        )
    )

    console.print(
        Align.center(
            "Xóa dữ liệu theo MSV",
            style="cyan",
        )
    )

    while True:
        msv = Prompt.ask("Nhập Mã sinh viên muốn xoá")
        ok=manager.delete_by_msv(msv)

        if ok:
            console.print(f"[bold green]Đã xóa thành công sinh viên {msv}[/bold green]")
            manager.load_data()
            time.sleep(1)
            break
        else:
            console.print(f"[bold red]MSV {msv} không tồn tại[/bold red]")

    console.clear()
    print_data()


def main_menu():
    manager.load_data()
    console.clear()
    console.print(
        Align.center(
            Panel(
                "[bold cyan]Classroom Data Manager[/bold cyan]\n"
                "v0.1 by Team HDH",
                expand=False,
            )
        )
    )

    console.print(
        Align.center(
            Panel(
                "[M] Xem dữ liệu lớp\n"
                "[0] Thoát chương trình",
                title="Menu chính",
                expand=False,
            )
        )
    )

    choice = Prompt.ask(
        "Chọn một nút",
        choices=["M", "0"],
        default="M",
    )

    if choice == "M":
        console.print("Chuyển đến dữ liệu sau 1s...")
        time.sleep(1)
        print_data()
    else:
        exit()

main_menu()
