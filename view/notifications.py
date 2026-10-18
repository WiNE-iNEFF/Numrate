# -*- coding: utf-8 -*-

from PySide2.QtCore import (
    QTimer,
    QPoint,
    QObject,
    QAbstractAnimation,
    QPropertyAnimation,
    QEasingCurve
)
from PySide2.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QFrame
)


class Notification(QFrame):
    COLORS = {
        "error": "#c0392b",
        "warning": "#f39c12",
        "success": "#27ae60",
        "info": "#3498db"
    }

    def __init__(self, parent, text, notif_type="info"):
        super().__init__(parent)

        self.setFixedSize(300, 65)
        self.setStyleSheet(f"""
        QFrame {{
            background-color: {self.COLORS[notif_type]};
            border-radius: 10px;
        }}

        QLabel {{
            color: white;
            font-size: 10pt;
            background: transparent;
        }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        label = QLabel(text)
        label.setWordWrap(True)
        layout.addWidget(label)


class NotificationManager(QObject):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.notifications = []

    def show_notification(self, text, notif_type="info", duration=5000):
        notif = Notification(self.parent, text, notif_type)

        self.notifications.append(notif)
        notif.show()

        self.reposition()

        target_pos = notif.pos()
        start_pos = QPoint(self.parent.width(), target_pos.y())

        notif.anim = QPropertyAnimation(notif, b"pos")
        notif.anim.setDuration(250)
        notif.anim.setStartValue(start_pos)
        notif.anim.setEndValue(target_pos)
        notif.anim.setEasingCurve(QEasingCurve.OutCubic)
        notif.anim.start()


        QTimer.singleShot(duration, lambda: self.remove_notification(notif))

    def remove_notification(self, notif):
        if notif not in self.notifications:
            return

        notif.leaving = True
        end_pos = QPoint(self.parent.width(), notif.y())

        notif.anim = QPropertyAnimation(notif, b"pos")
        notif.anim.setDuration(250)
        notif.anim.setStartValue(notif.pos())
        notif.anim.setEndValue(end_pos)
        notif.anim.setEasingCurve(QEasingCurve.InCubic)

        def finish():
            if notif in self.notifications:
                self.notifications.remove(notif)
                notif.deleteLater()
                self.reposition()

        notif.anim.finished.connect(finish)
        notif.anim.start()

    def reposition(self):
        margin = 15
        spacing = 10

        y = self.parent.height() - margin

        for notif in reversed(self.notifications):
            y -= notif.height()
            target = QPoint(self.parent.width() - notif.width() - margin, y)

            anim = getattr(notif, "anim", None)
            if (anim is not None
                    and anim.state() == QAbstractAnimation.Running
                    and not getattr(notif, "leaving", False)):
                anim.setEndValue(target)
            else:
                notif.move(target)

            y -= spacing
