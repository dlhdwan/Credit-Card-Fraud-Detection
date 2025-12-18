# 📊 Thông tin Chi tiết về Bộ dữ liệu (Dataset Information)

Dưới đây là bản mô tả chi tiết về bộ dữ liệu mô phỏng giao dịch thẻ tín dụng được sử dụng trong dự án.

---

## 1. Tổng quan Dự án (Project Overview)
Bộ dữ liệu chứa các giao dịch thẻ tín dụng mô phỏng, bao gồm cả giao dịch hợp lệ và giao dịch gian lận trong khoảng thời gian từ **01/01/2019 đến 31/12/2020**.

* **Quy mô:** Bao gồm giao dịch của **1.000 khách hàng** với **800 cửa hàng/đơn vị thụ hưởng**.
* **Nguồn gốc:** Dữ liệu được tạo bởi công cụ mô phỏng **Sparkov Data Generation** ( Brandon Harris).
* **Cơ chế mô phỏng:** Sử dụng thư viện `Faker` kết hợp với các hồ sơ người dùng (profiles) cụ thể để tạo ra các phân phối giao dịch thực tế dựa trên độ tuổi, giới tính và khu vực sinh sống (thành thị/nông thôn).

---

## 2. Danh mục các Đặc trưng (Data Features)

### 📌 Thông tin Giao dịch & Mục tiêu
* **`trans_date_trans_time`**: Ngày và giờ xảy ra giao dịch.
* **`amt`**: Số tiền của giao dịch (USD).
* **`trans_num`**: Mã định danh duy nhất của giao dịch.
* **`unix_time`**: Thời gian giao dịch dưới định dạng UNIX timestamp.
* **`is_fraud`**: **[Biến mục tiêu]** Giá trị `1` nếu là gian lận, `0` nếu là giao dịch hợp lệ.

### 👤 Thông tin Chủ thẻ (Customer Info)
* **`cc_num`**: Số thẻ tín dụng của khách hàng.
* **`first` / `last`**: Họ và tên của chủ thẻ.
* **`gender`**: Giới tính của chủ thẻ.
* **`dob`**: Ngày tháng năm sinh của chủ thẻ (dùng để tính tuổi).
* **`job`**: Nghề nghiệp của chủ thẻ.

### 📍 Thông tin Địa lý (Location Info)
* **`street` / `city` / `state` / `zip`**: Địa chỉ nơi cư trú của chủ thẻ.
* **`lat` / `long`**: Tọa độ địa lý (Vĩ độ/Kinh độ) của chủ thẻ.
* **`city_pop`**: Dân số tại thành phố của chủ thẻ (phản ánh quy mô khu vực).
* **`merch_lat` / `merch_long`**: Tọa độ địa lý của cửa hàng nơi giao dịch diễn ra.

### 🛍️ Thông tin Cửa hàng (Merchant Info)
* **`merchant`**: Tên của cửa hàng/đơn vị thụ hưởng.
* **`category`**: Loại hình kinh doanh/danh mục giao dịch (ví dụ: thực phẩm, mua sắm, xăng dầu...).

---

## 3. Các đặc trưng nâng cao được xây dựng (Feature Engineering)
Dựa trên dữ liệu gốc, mô hình sử dụng thêm các biến tự xây dựng để tăng độ chính xác:

* **Khoảng cách (`distance_km`)**: Khoảng cách từ tọa độ chủ thẻ đến cửa hàng.
* **Tần suất (`txn_count_1h/24h`)**: Số lượng giao dịch trong các cửa sổ thời gian gần nhất.
* **Chỉ số bất thường (`amt_zscore_7d`)**: Độ lệch của số tiền giao dịch so với trung bình chi tiêu hàng tuần.
* **Thời điểm rủi ro (`is_night`/`is_weekend`)**: Phân loại giao dịch theo thời gian nhạy cảm.

---
**Nguồn tham khảo:** [Kaggle Fraud Detection Dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection)