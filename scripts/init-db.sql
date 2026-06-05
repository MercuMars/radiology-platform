-- Initialize the radiology platform database
-- This script runs when the PostgreSQL container starts for the first time

-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS cases (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    patient_id VARCHAR(100),
    modality VARCHAR(50),
    body_part VARCHAR(100),
    diagnosis TEXT,
    teaching_points TEXT,
    difficulty_level INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS case_images (
    id SERIAL PRIMARY KEY,
    case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
    dicom_instance_id VARCHAR(255),
    image_type VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_cases_modality ON cases(modality);
CREATE INDEX IF NOT EXISTS idx_cases_body_part ON cases(body_part);
CREATE INDEX IF NOT EXISTS idx_cases_difficulty ON cases(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_case_images_case_id ON case_images(case_id);

-- Insert sample data (optional)
INSERT INTO cases (title, description, patient_id, modality, body_part, diagnosis, teaching_points, difficulty_level)
VALUES
    ('肺部CT扫描示例', '55岁男性，长期吸烟史，咳嗽咳痰3个月', 'P001', 'CT', '胸部', '右肺上叶占位性病变，考虑肺癌可能', '1. 注意观察肺窗和纵隔窗\n2. 测量病灶大小\n3. 观察有无淋巴结转移', 3),
    ('头部MRI检查', '45岁女性，头痛头晕1周', 'P002', 'MRI', '头部', '左侧颞叶异常信号，考虑脑梗塞', '1. T1WI和T2WI信号特点\n2. DWI序列弥散受限\n3. 增强扫描强化方式', 2),
    ('膝关节X光片', '30岁男性，运动后膝关节疼痛', 'P003', 'X-Ray', '膝关节', '未见明显骨折征象', '1. 正侧位片观察\n2. 关节间隙测量\n3. 软组织肿胀评估', 1)
ON CONFLICT DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO radio;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO radio;
