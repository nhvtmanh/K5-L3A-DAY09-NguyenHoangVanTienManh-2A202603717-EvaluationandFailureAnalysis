# Đánh giá agent hoàn tiền và chặn regression

Bổ sung taxonomy, judge calibration, grader tiền/approval và FM-08, paired bootstrap,
slice gate, pass^k và integrity/ratchet. Giữ nguyên Lab 8, variant/trap và test được cung cấp.
Report sinh qua CLI; v1 baseline `E-swarm-20261118-3453`, v2 `E-swarm-20261118-e36a`.

## Kiểm tra local

- Host contracts: 57 passed, 299 deselected in 3.71s
- Core tests: 21 passed, 335 deselected in 5.78s
- Advanced tests: 30 passed, 326 deselected in 1.00s
- M3 detection: detection 100.00% (target >=80%) · false alarms 0.00% (target <=10%)

## Gate v1

```text
gate: PR E-seeded_regression-20261118-3453 vs main E-swarm-20261118-3453 · eval set 3453548c0106
  approval_bypass        0        {"max": 0}                                                            ok
  secret_leak            0        {"max": 0}                                                            ok
  db_fact_kept           0.9286   {"min": 0.95}                                                         warn
  refund_amount_correct  0.8571   {"min": 0.95, "no_significant_drop": true} Δ -0.129 CI [-0.315, +0.000] BLOCK
  pass_rate              0.7143   {"min": 0.85, "no_significant_drop": true} Δ -0.271 CI [-0.500, -0.057] BLOCK
  pass_5                 0.7143   {"min": 0.8}                                                          warn
  cost_per_success       81.202   {"max_increase": 0.1}                                                 warn
  reply_amount_correct   0.7857   {"min": 1.0}                                                          BLOCK
  proposal_amount_correct 0.7857   {"min": 0.95}                                                         warn
exit 1 — blocked: refund_amount_correct, pass_rate, reply_amount_correct
```

Fixed và PR swarm exit 0; baseline sanity exit 0.

## A/A và mutation v2

```text
metric                 spec seeds  alt seeds    delta
approval_bypass                 0          0  +0.0000
secret_leak                     0          0  +0.0000
db_fact_kept               0.9786     0.9786  +0.0000
refund_amount_correct      0.9786     0.9786  +0.0000
pass_rate                  0.9786     0.9786  +0.0000
reply_amount_correct          1.0        1.0  +0.0000
proposal_amount_correct     0.9786     0.9786  +0.0000
pass_5                     0.8929     0.8929  +0.0000
pass_at_1                  0.9786     0.9786  +0.0000
pass_hat_1                 0.9786     0.9786  +0.0000
pass_at_3                     1.0        1.0  +0.0000
pass_hat_3                 0.9357     0.9357  +0.0000
pass_at_5                     1.0        1.0  +0.0000
pass_hat_5                 0.8929     0.8929  +0.0000
cost_per_success          50.8077    50.8077  +0.0000
```

```text
fixed                expect merge got merge ok
  honest_refactor      expect merge got merge ok
  seeded_regression    expect block got block ok          refund_amount_correct, pass_rate, pass_hat_5, reply_amount_correct, slice:denial/pass_rate, slice:money_movement/pass_rate, slice:adversarial/pass_rate
  slice_regression     expect block got block ok          slice:money_movement/pass_rate
  flaky_regression     expect block got block ok          pass_rate, pass_hat_5, slice:money_movement/pass_rate
mutation score 3/3 · false alarms 0
```

## Bốn trap


evaluator_errors_as_nan:

```text
  INTEGRITY PR: invalid row score E-014@11/refund_amount_correct
exit 1 — blocked: integrity
```

dropped_failing_rows:

```text
  INTEGRITY PR: row/item count differs from manifest
exit 1 — blocked: integrity
```

cherry_picked_seeds:

```text
  INTEGRITY PR: missing aggregate pass_hat_5
exit 1 — blocked: integrity
```

loosened_spec:

```text
  INTEGRITY ratchet: db_fact_kept loosened min
exit 1 — blocked: integrity
```

## Trước khi nộp

- Commit các report bắt buộc bằng git add -f vì reports/ bị ignore.
- Đưa các file nền Lab 8 đang untracked vào repo, giữ nguyên nội dung, để CI có đủ dependency.
- Mở PR starter/d09 → main và xác nhận eval-gate, eval-gate-v2 xanh.
- Đối chiếu năm anchor với coding sheet trên lớp; key ẩn không có trong repo.
- Local chưa chạy hidden grader, chưa chứng minh chất lượng trên model/người dùng thật.
