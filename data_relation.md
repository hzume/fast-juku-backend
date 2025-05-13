# 現状

## 各kindについてのサマリ

- 全itemは`school_id`、`timestamp`を持つ

- `MetaModel`
    - `record_type=meta`
    - `id=school_id`: `school_name`によって定まるhash

- `TeacherModel`
    - `record_type="teacher"`
    - `id=UUID`: `display_name`と`school_id`によって定まるhash
    - `sub`

- `MonthlyAttendanceModel`
    - `record_type="attendance#2023-07"`
    - `id=teacher_id`
    - `TimeslotMap`の列を持ち、それを集約して月間給与等を計算する
    - `TeacherModel`の各要素を持っている（その月に計算する時給などを保存）


## 用いているクエリ
- `MetaRepo`
    - `create`: SAVE
    - `get`: GET (`record_type=meta`, `id=school_id`)
    - `list`: QUERY (`record_type=meta`)
    - `update`: GET (`record_type=meta`, `id=school_id`), SAVE
    - `delete`: GET (`record_type=meta`, `id=school_id`), DELETE

- `TeacherRepo`
    - `create`: SAVE
    - `get`: GET (`record_type=teacher`, `id=id`)
    - `list`: QUERY (`record_type=meta`, filter:`school_id`)
    - `get_from_sub`: QUERY (`record_type=teacher`, filter:`sub`)
    - `update`: GET (`record_type=teacher`, `id=id`),  SAVE
    - `delete`: GET (`record_type=teacher`, `id=id`), DELETE

- `MonthlyAttendanceRepo`
    - `create`: SAVE
    - `create_list`: pass
    - `get`: GET (`record_type=attendance#2023-07`, `id=id`)
    - `list_monthly`: @school_id_index QUERY(`school_id=school_id`, `record_type=attendance#2023-07`)
    - `list_between`: @schol_id_index QUERY(`school_id=school_id`, between:`record_type=attendance#2023-01~attendance#2023-12`)
    - `update`: GET (`record_type=attendance#2023-07`, `id=id`) SAVE
    - `delete`: GET (`record_type=attendance#2023-07`, `id=id`) DELETE

# どうあるべきか
- `SchoolModel`
    - `list`を実現するために`school_id`のリストを持つitemを作成し、create,delete時に更新する(p_key="meta_list",s_key=0)
    - p_key={school_id}
    - s_key="school"

- `SchoolListModel`
    - p_key="school_list"
    - s_key="0"

- `TeacherModel`
    - p_key={school_id}
    - s_key="teacher#{teacher_id}"

- `TeacherListModel`
    - p_key={school_id}
    - s_key="teachers"

- `TeacherShiftModel`
    - p_key={teacher_id}
    - s_key="YYYY-MM"

- `StudentModel`

- `StudentScheduleModel`
    - p_key={student_id}
    - s_key="YYYY-MM"