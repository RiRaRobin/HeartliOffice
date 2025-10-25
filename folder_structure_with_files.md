# 📁 Project Folder Structure (with files)

Legend:
🐍 Python 📈 CSV 🧠 Pickle 📄 Markdown 📃 Text 🧾 JSON 🗄️ DB 🖼️ Image 📑 PDF 📓 Notebook ℹ️ README

```text
Heartli_OfficeTool/
├── 📄 PROJEKTPLAN.md
├── 📑 PROJEKTPLAN.pdf
├── ℹ️ README.md
├── 🐍 app.py
├── 📄 folder_structure.md
├── 📄 folder_structure_with_files.md
├── 🐍 path_config.py
├── 📃 requirements.txt

├── 00_data/
│   ├── 00_examples/
│   │   📄 example_meeting.yaml
│   │   📄 example_questions.yaml
│   │   📄 example_task.yaml
│   ├── 01_tasks/
│   │   ├── 01_active/
│   │   │   📄 T-2025-10-25-001.yaml
│   │   │   📄 T-2025-10-25-002.yaml
│   │   │   📄 T-2025-10-25-003.yaml
│   │   │   📄 T-2025-10-25-004.yaml
│   │   │   📄 T-2025-10-25-005.yaml
│   │   │   📄 T-2025-10-25-006.yaml
│   │   │   📄 T-2025-10-25-007.yaml
│   │   │   📄 T-2025-10-25-008.yaml
│   │   │   📄 T-2025-10-25-009.yaml
│   │   │   📄 T-2025-10-25-010.yaml
│   │   │   📄 T-2025-10-25-011.yaml
│   │   ├── 02_archive/
│   ├── 02_meetings/
│   │   ├── 01_active/
│   │   ├── 02_archive/
│   ├── 03_questions/
│   │   ├── 01_active/
│   │   ├── 02_archive/

├── 01_src/
│   ├── 00_common/
│   │   🐍 ids.py
│   │   🐍 io_yaml.py
│   ├── 01_tasks/
│   │   🐍 task_dialog.py
│   │   📄 task_dialog.ui
│   │   🐍 tasks_service.py
│   ├── 02_meetings/
│   ├── 03_questions/

├── 02_utils/
│   🐍 create_requirements.py
│   🐍 make_folder_structure_md.py

├── 03_legacy/

├── src/
│   🐍 __init__.py
│   ├── common/
│   │   🐍 __init__.py
│   ├── meetings/
│   │   🐍 __init__.py
│   ├── questions/
│   │   🐍 __init__.py
│   ├── tasks/
│   │   🐍 __init__.py

├── ui/
│   📄 main_window.ui
```
