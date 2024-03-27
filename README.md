# Kiến trúc triển khai
![image](https://github.com/Quanghuy99/ChatGPT_RAG/assets/30777550/ea90b883-69b6-4b53-9e44-402a53feddb3)

# Giải thích một vài phần quan trọng
## File config
![image](https://github.com/Quanghuy99/ChatGPT_RAG/assets/30777550/3dd1d1c3-48cd-4a90-a7c8-2d0941e827d9)

## Các bước chạy:
1. chạy file create_db.py (embedding kiến thức trong file.pdf và lưu vào db vector)
2. chạy file app.py
   ![image](https://github.com/Quanghuy99/ChatGPT_RAG/assets/30777550/03c6c173-8f04-4e28-9fbb-15d6caff0bbf)
    {
  "InputText": "string", # text chat
  "IdRequest": "string", # id của ng dùng ( cái này nhập bất kỳ để test)
  "NameBot": "string", # cái này sau mk sẽ chia theo loại bot để tư vấn chi tiết hơn( cái này nhập bất kỳ để test)
  "User": "string", # để phân biệt đoạn chat giữa các users ( cái này nhập bất kỳ để test)
  "Image": "string", # Convert ảnh qua base64 rồi truyền vào. Phần này để phân loại ảnh sản phẩm mà khách hàng muốn mua || link convert imae to base64: https://base64.guru/converter/encode/image
  "Voice": "string", # phần này sẽ từ voice quan text như inputtext bên trên
  }
