create database QuanLiThueBoardgame
go
use QuanLiThueBoardgame
go

create table TheLoai
(
	MSTL varchar(10) primary key,
	TenTheLoai varchar(50),
	GhiChu varchar(50),
)

create table Boardgame
(
	MSBG varchar(10) primary key,
	TenBG varchar(50),
	MSTL varchar(10),
	SoNguoiChoi int,
	MucDo varchar(10),
	ThoiGian varchar(10),
	TacGia varchar(50),
	NXB varchar(50),
	NamSX int,
	MoTa varchar(100),
	LuatChoi varchar(100),
	PhienBan varchar(20),
	GiaThue int,
	TinhTrang varchar(50),
	GhiChu varchar(50),
	constraint FK_Boardgame_TheLoai foreign key (MSTL) references dbo.TheLoai (MSTL)
)

create table KhachHang
(
	MSKH varchar(10) primary key,
	HoTen varchar(50),
	SDT varchar(10),
	Email varchar(50),
	DiaChi varchar(100),
	DiemTichLuy int,
)

create table DatCho 
(
	MDC varchar(10) primary key,
	MSBG varchar(10),
	MSKH varchar(10),
	SoNgayThue int,
	TienThue int,
	TienCoc int, 
	NgayDatCho smalldatetime,
	GioDatCho smalldatetime,
	TrangThai varchar(50),
)
create table Thue 
(
	MT varchar(10) primary key,
	MDC varchar(10),
	NgayBatDau smalldatetime,
	NgayKetThuc smalldatetime,
)

alter table DatCho add constraint FK_MSKH_DatCho foreign key (MSKH) references dbo.KhachHang (MSKH)
alter table DatCho add constraint FK_MSBG_DatCho foreign key (MSBG) references dbo.Boardgame (MSBG)
alter table Thue add constraint FK_MDC_Thue foreign key (MDC) references dbo.DatCho (MDC)


