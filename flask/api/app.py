from flask import Flask, request, render_template, send_file
from PIL import Image, ImageEnhance
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

# 设置路由和视图函数
@app.route('/', methods=['GET', 'POST'])
def process_image():
    if request.method == 'POST':
        # 获取上传的图片文件
        image_file = request.files['image']
        
        # 保存上传的图片文件
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)
        
        # 打开上传的图片
        image = Image.open(image_path)
        
        # 图片优化处理
        enhanced_image = enhance_image(image)
        
        # 保存优化后的图片
        enhanced_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'enhanced_' + image_file.filename)
        enhanced_image.save(enhanced_image_path)
        
        # 删除上传的图片
        os.remove(image_path)
        
        # 渲染结果页面
        return render_template('result.html', image_path=enhanced_image_path)
    
    # 渲染上传页面
    return render_template('upload.html')

def enhance_image(image):
    # 图片优化处理逻辑，这里使用了图像增强的示例
    enhancer = ImageEnhance.Sharpness(image)
    enhanced_image = enhancer.enhance(2.0)  # 增强图片的锐度
    return enhanced_image

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    # 下载优化后的图片
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
