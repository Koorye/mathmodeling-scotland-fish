import pyautogui
import time

# x=1754, y=245, 选择年份按钮
# x=1756, y=340, 预览按钮
# x=1828, y=343, 确定按钮
# x=1264, y=766, 导出 excel 按钮

if __name__ == '__main__':
    time.sleep(3)
    for i in range(10):
        # 选择年份按钮 -> 方向下键 -> 回车键
        pyautogui.moveTo(1754, 245, .1)
        pyautogui.click(duration=.1)
        pyautogui.keyDown('down')
