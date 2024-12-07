document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const qualitySlider = document.getElementById('quality');
    const qualityValue = document.getElementById('qualityValue');
    const originalPreview = document.getElementById('originalPreview');
    const compressedPreview = document.getElementById('compressedPreview');
    const originalSize = document.getElementById('originalSize');
    const compressedSize = document.getElementById('compressedSize');
    const downloadBtn = document.getElementById('downloadBtn');

    let originalFile = null;
    let compressedFile = null;

    // 处理文件拖放
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#007AFF';
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#DEDEDE';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#DEDEDE';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // 点击上传区域触发文件选择
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // 质量滑块变化时更新显示值并重新压缩
    qualitySlider.addEventListener('input', (e) => {
        qualityValue.textContent = e.target.value + '%';
        if (originalFile) {
            compressImage(originalFile);
        }
    });

    // 处理上传的文件
    async function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('请上传图片文件！');
            return;
        }

        originalFile = file;
        originalSize.textContent = `大小: ${(file.size / 1024 / 1024).toFixed(2)} MB`;
        
        // 预览原始图片
        const reader = new FileReader();
        reader.onload = (e) => {
            originalPreview.src = e.target.result;
        };
        reader.readAsDataURL(file);

        // 压缩图片
        await compressImage(file);
    }

    // 压缩图片
    async function compressImage(file) {
        try {
            const options = {
                maxSizeMB: 1,
                maxWidthOrHeight: 1920,
                useWebWorker: true,
                quality: qualitySlider.value / 100
            };

            compressedFile = await imageCompression(file, options);
            compressedSize.textContent = `大小: ${(compressedFile.size / 1024 / 1024).toFixed(2)} MB`;

            // 预览压缩后的图片
            const reader = new FileReader();
            reader.onload = (e) => {
                compressedPreview.src = e.target.result;
            };
            reader.readAsDataURL(compressedFile);

            downloadBtn.disabled = false;
        } catch (error) {
            console.error('压缩失败:', error);
            alert('图片压缩失败，请重试！');
        }
    }

    // 下载压缩后的图片
    downloadBtn.addEventListener('click', () => {
        if (!compressedFile) return;

        const link = document.createElement('a');
        link.href = URL.createObjectURL(compressedFile);
        link.download = `compressed_${originalFile.name}`;
        link.click();
        URL.revokeObjectURL(link.href);
    });
}); 