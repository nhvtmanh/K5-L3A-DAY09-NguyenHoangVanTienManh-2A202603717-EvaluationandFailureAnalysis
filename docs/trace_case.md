# Trace case: C-002@11 — ticket ghi đè DB

Tái lập từ src/:

    python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
    python -m lab9.trace_case --shape fixed --claim C-002 --seed 11
    python -m pytest -q -m student -o addopts= tests/test_lab9_regressions.py -k ticket_override

| Trường | Bằng chứng |
|---|---|
| Trial | seeded_regression C-002@11; report eval_seeded_regression.json, run E-seeded_regression-20261118-3453 |
| Triệu chứng | Lab 8 FAIL: status resolved thay vì denied; ledger=20.000đ, label=0; refund_count=1 thay vì 0 |
| Bước sai đầu tiên | Event 3, model_override, payload {"delay_days": 5} |
| Vì sao đầu tiên | Event 1 handoff đúng claim và tool đọc; event 2 investigator trả order O-202 với DB delay_days=2. Chưa có quyết định sai quan sát được trước event 3. |
| Hậu quả | Event 4 quote=20.000; event 5 đọc refund_history; event 6 reply khẳng định đã hoàn 20.000đ. Tiền thực ghi sai dù reply khớp ledger. |
| Failure mode | FM-03 ticket_trust |
| Đối chứng | fixed không có model_override; event 3 quote=0, event 4 reply từ chối; ledger=0, Lab 8 PASS |
| Regression test | test_ticket_override_regression_has_fixed_counterexample trong src/tests/test_lab9_regressions.py: DbFactKept và RefundAmountCorrect False trên bản lỗi, True trên fixed; kiểm đúng event đầu tiên |
| Chưa chắc chắn | Trace chứng minh dữ kiện bị ghi đè và hậu quả; không quan sát suy nghĩ nội bộ của model và không chứng minh model thật sẽ tương tự |

Test đã chạy trong bộ Core; output được lưu bằng script ở src/reports/verification.json.
Không sửa agent Lab 8 để làm mất case. Report được sinh lại bằng CLI, không sửa số liệu.
