# src/desktop/gui/tabs/data_io_tab.py
"""
Data I/O tab implementation
Created: 2025-01-31 14:32:45
Author: GingaDza
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QMessageBox,
    QLabel, QProgressBar
)
from PySide6.QtCore import Qt
import json
import os

class DataIOTab(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)  # 正しい親ウィジェットの指定
        self.data_manager = data_manager
        self.setup_ui()
    
    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        
        # ヘッダー部分
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # タイトル
        title = QLabel("データ入出力")
        title.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(title)
        
        layout.addWidget(header)
        
        # データエクスポート部分
        export_group = QWidget()
        export_layout = QVBoxLayout(export_group)
        export_layout.setContentsMargins(0, 0, 0, 0)
        
        export_label = QLabel("データエクスポート")
        export_label.setStyleSheet("font-weight: bold;")
        export_layout.addWidget(export_label)
        
        export_button = QPushButton("エクスポート")
        export_button.clicked.connect(self.export_data)
        export_layout.addWidget(export_button)
        
        layout.addWidget(export_group)
        
        # データインポート部分
        import_group = QWidget()
        import_layout = QVBoxLayout(import_group)
        import_layout.setContentsMargins(0, 0, 0, 0)
        
        import_label = QLabel("データインポート")
        import_label.setStyleSheet("font-weight: bold;")
        import_layout.addWidget(import_label)
        
        import_button = QPushButton("インポート")
        import_button.clicked.connect(self.import_data)
        import_layout.addWidget(import_button)
        
        layout.addWidget(import_group)
        
        # 進捗バー
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # スペーサー
        layout.addStretch()
    
    def export_data(self):
        """データのエクスポート"""
        try:
            # ファイル選択ダイアログ
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "データエクスポート",
                "",
                "JSONファイル (*.json)"
            )
            
            if not file_name:
                return
            
            # 進捗バーの表示
            self.progress.setVisible(True)
            self.progress.setValue(0)
            
            # データの収集
            data = {
                'metadata': {
                    'created_at': self.data_manager.created_at.isoformat(),
                    'created_by': self.data_manager.created_by,
                    'last_modified_at': self.data_manager.last_modified_at.isoformat(),
                    'last_modified_by': self.data_manager.last_modified_by
                },
                'groups': {},
                'users': {},
                'categories': {},
                'skills': {}
            }
            
            self.progress.setValue(20)
            
            # グループデータ
            for group_id, group in self.data_manager.groups.items():
                data['groups'][group_id] = {
                    'name': group.name,
                    'description': group.description,
                    'members': list(group.members)
                }
            
            self.progress.setValue(40)
            
            # ユーザーデータ
            for user_id, user in self.data_manager.users.items():
                data['users'][user_id] = {
                    'name': user.name,
                    'email': user.email,
                    'group_id': user.group_id,
                    'skill_levels': user.skill_levels
                }
            
            self.progress.setValue(60)
            
            # カテゴリーデータ
            for category_id, category in self.data_manager.categories.items():
                data['categories'][category_id] = {
                    'name': category.name,
                    'description': category.description,
                    'skills': list(category.skills)
                }
            
            self.progress.setValue(80)
            
            # スキルデータ
            for skill_id, skill in self.data_manager.skills.items():
                data['skills'][skill_id] = {
                    'name': skill.name,
                    'category_id': skill.category_id,
                    'description': skill.description
                }
            
            # JSONファイルの保存
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.progress.setValue(100)
            QMessageBox.information(
                self,
                "エクスポート完了",
                "データのエクスポートが完了しました。"
            )
            
        except Exception as e:
            QMessageBox.warning(
                self,
                "エクスポートエラー",
                f"データのエクスポート中にエラーが発生しました：\n{str(e)}"
            )
        
        finally:
            self.progress.setVisible(False)
    
    def import_data(self):
        """データのインポート"""
        try:
            # ファイル選択ダイアログ
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "データインポート",
                "",
                "JSONファイル (*.json)"
            )
            
            if not file_name:
                return
            
            # 確認ダイアログ
            reply = QMessageBox.question(
                self,
                "データインポート",
                "既存のデータは上書きされます。続行しますか？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
            
            # 進捗バーの表示
            self.progress.setVisible(True)
            self.progress.setValue(0)
            
            # JSONファイルの読み込み
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.progress.setValue(20)
            
            # データのクリア
            self.data_manager.groups.clear()
            self.data_manager.users.clear()
            self.data_manager.categories.clear()
            self.data_manager.skills.clear()
            
            self.progress.setValue(40)
            
            # グループの復元
            for group_id, group_data in data['groups'].items():
                group = self.data_manager.groups[group_id] = Group(
                    id=group_id,
                    name=group_data['name'],
                    description=group_data['description']
                )
                for member_id in group_data['members']:
                    group.add_member(member_id)
            
            self.progress.setValue(60)
            
            # ユーザーの復元
            for user_id, user_data in data['users'].items():
                user = self.data_manager.users[user_id] = User(
                    id=user_id,
                    name=user_data['name'],
                    email=user_data['email'],
                    group_id=user_data['group_id']
                )
                user.skill_levels = user_data['skill_levels']
            
            self.progress.setValue(80)
            
            # カテゴリーとスキルの復元
            for category_id, category_data in data['categories'].items():
                category = self.data_manager.categories[category_id] = Category(
                    id=category_id,
                    name=category_data['name'],
                    description=category_data['description']
                )
                for skill_id in category_data['skills']:
                    category.add_skill(skill_id)
            
            for skill_id, skill_data in data['skills'].items():
                self.data_manager.skills[skill_id] = Skill(
                    id=skill_id,
                    name=skill_data['name'],
                    category_id=skill_data['category_id'],
                    description=skill_data['description']
                )
            
            # メタデータの更新
            self.data_manager.created_at = datetime.fromisoformat(data['metadata']['created_at'])
            self.data_manager.created_by = data['metadata']['created_by']
            self.data_manager.last_modified_at = datetime.fromisoformat(data['metadata']['last_modified_at'])
            self.data_manager.last_modified_by = data['metadata']['last_modified_by']
            
            self.progress.setValue(100)
            
            # 変更通知
            self.data_manager.groups_changed.emit()
            self.data_manager.users_changed.emit()
            self.data_manager.categories_changed.emit()
            self.data_manager.skills_changed.emit()
            
            QMessageBox.information(
                self,
                "インポート完了",
                "データのインポートが完了しました。"
            )
            
        except Exception as e:
            QMessageBox.warning(
                self,
                "インポートエラー",
                f"データのインポート中にエラーが発生しました：\n{str(e)}"
            )
        
        finally:
            self.progress.setVisible(False)