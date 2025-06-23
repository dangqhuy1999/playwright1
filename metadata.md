Ví dụ về một dictionary metadata chuẩn cho một chunk
chunk_metadata = {
    # 1. METADATA CẤP CAO & ID DUY NHẤT (QUAN TRỌNG NHẤT)
    "chunk_id": "unique_id_for_this_chunk",  # ID duy nhất của chunk (Qdrant tự tạo nếu không cung cấp)
    "document_id": "unique_id_of_original_document", # ID của tài liệu gốc (PDF, Webpage, Database Row, etc.)
    "global_content_id": "some_system_wide_id", # Nếu có một ID tổng thể cho nội dung trong hệ thống của bạn

    # 2. METADATA CỤ THỂ THEO KHÁCH HÀNG (QUAN TRỌNG ĐỂ PHÂN QUYỀN/LỌC)
    "customer_id": "customer_A_uuid_or_id", # ID của khách hàng sở hữu dữ liệu này
    "project_id": "project_xyz_for_customer_A", # ID dự án nếu khách hàng có nhiều dự án
    "access_level": ["public", "internal_team_A", "premium_users"], # Mức độ truy cập (dùng cho bộ lọc bảo mật)
    "tags_customer_specific": ["marketing", "legal_docs", "2024_campaign"], # Tags do khách hàng định nghĩa

    # 3. METADATA CỤ THỂ THEO NGUỒN DỮ LIỆU
    "source_type": "web_content",  # web_content, pdf_content, database_content, docx_content, image_content, md_content, csv_content
    "source_url": "https://example.com/product_X_manual.html", # URL cho web/PDF/online docs
    "file_path": "/path/to/local/file.docx", # Đường dẫn file cục bộ (nếu có)
    "image_description": "description of content in image", # Mô tả nội dung ảnh (nếu từ ảnh)
    "page_number": 5, # Số trang (cho PDF/DOCX)
    "html_element_id": "product_specs_div", # ID của element HTML gốc (nếu trích từ HTML cụ thể)
    "md_source_path": "/path/to/markdown_file.md", # Đường dẫn file markdown gốc

    # 4. METADATA MÔ TẢ CHUNK VÀ NỘI DUNG TỔNG THỂ
    "document_title": "Product X User Manual", # Tiêu đề của tài liệu gốc
    "section_title": "Installation Guide", # Tiêu đề của phần mà chunk thuộc về
    "heading_path": "Product X > Technical Specs > Installation", # Đường dẫn cấu trúc theo tiêu đề
    "content_type": "paragraph", # Loại nội dung của chunk (paragraph, table, list, code_block, image_caption, chart_description)
    "author": "John Doe",
    "publish_date": "2024-05-15",
    "last_modified_date": "2024-06-01",
    "language": "vi", # Ngôn ngữ của nội dung
    "tags": ["machinery", "welding", "safety"], # Các thẻ chung (có thể dùng để lọc hoặc hiển thị)
    "summary": "This chunk describes the safety precautions for operating welding machinery.", # Tóm tắt ngắn gọn của chunk

    # 5. METADATA BỔ SUNG ĐẶC THÙ CHO LĨNH VỰC "CƠ KHÍ HÓA"
    "product_name": "Model XYZ Welding Machine",
    "model_number": "XYZ-1000",
    "part_number": "P-45678",
    "material_type": "Stainless Steel",
    "machine_type": "CNC Mill",
    "safety_related": True, # Boolean: true nếu chunk liên quan đến an toàn
    "regulatory_compliance": ["ISO 9001", "CE Certified"], # Các tiêu chuẩn tuân thủ
    "component_name": "Hydraulic Pump", # Nếu chunk mô tả một bộ phận cụ thể
    "version": "1.2.0" # Phiên bản của tài liệu/sản phẩm
}
-- 
 
