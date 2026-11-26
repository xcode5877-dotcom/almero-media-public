# Wedbook — مصدر الدفعة الأولى (مسودة بدون لوغو)
- `carousel.html?s=1..5` → `node shot.js <هاد المجلد>` (كاروسيل 4:5).
- `node render.js reel_a.html out.mp4` / `reel_b.html` (ريل 9:16، 30fps).
- موسيقى: `python3 music.py out.wav <مدة> "<ضربات>" <seed>` (مولّدة بالكود، بدون حقوق)، وبعدين ffmpeg loudnorm I=-14.
- **اللوغو:** بدّل `.logo-slot` (الزاوية + شريحة الختام) بـ`<img>` من `nmd-hub/brand/wedbook/logo.png` وأعد الرندر.
- الألوان مؤقتة ومحايدة (مش الأسود والذهبي)، الخط Cairo للمسودات بس.
