"""
2_logistic_regression_practice.py

scikit-learn의 LogisticRegression 연습용 스크립트.
유방암(breast cancer) 데이터셋을 사용해 종양이 악성/양성인지 이진 분류합니다.

배울 수 있는 것:
- 데이터 스케일링(StandardScaler)이 로지스틱 회귀에 왜 중요한지
- train/test 분리 & 학습
- 정확도 / classification_report / confusion_matrix / ROC-AUC
- predict_proba (확률 예측)
- 회귀 계수(coef_) 해석
- 정규화 강도 파라미터 C 바꿔가며 실험
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)


def main():
    # 1. 데이터 불러오기
    data = load_breast_cancer()
    X, y = data.data, data.target
    feature_names = data.feature_names
    class_names = data.target_names  # ['malignant', 'benign']

    print(f"[데이터] 샘플 수: {X.shape[0]}, 특성 수: {X.shape[1]}, 클래스: {list(class_names)}\n")

    # 2. train/test 분리
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. 스케일링 (로지스틱 회귀는 특성의 스케일에 민감하므로 표준화 필수!)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4. 모델 학습
    clf = LogisticRegression(max_iter=5000, random_state=42)
    clf.fit(X_train_scaled, y_train)

    y_pred = clf.predict(X_test_scaled)
    y_proba = clf.predict_proba(X_test_scaled)[:, 1]  # 클래스 1(양성)일 확률

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)
    print(f"[모델 성능] 정확도: {acc:.4f}, ROC-AUC: {auc:.4f}\n")

    print("[classification_report]")
    print(classification_report(y_test, y_pred, target_names=class_names))

    print("[confusion_matrix]")
    print(confusion_matrix(y_test, y_pred), "\n")

    # 5. 예측 확률 예시 (앞 5개 샘플)
    print("[샘플별 예측 확률 예시 (앞 5개)]")
    for i in range(5):
        print(f"  실제={class_names[y_test[i]]:10s} 예측={class_names[y_pred[i]]:10s} "
              f"양성일 확률={y_proba[i]:.3f}")

    # 6. 회귀 계수 해석 - 어떤 특성이 결과에 큰 영향을 주는지
    coef = clf.coef_[0]
    top_idx = np.argsort(np.abs(coef))[::-1][:5]
    print("\n[영향력 큰 특성 Top 5 (|계수| 기준)]")
    for i in top_idx:
        direction = "양성 쪽 확률 증가" if coef[i] > 0 else "악성 쪽 확률 증가"
        print(f"  {feature_names[i]:25s} : coef={coef[i]: .4f}  ({direction})")

    # 7. 정규화 강도 C 값을 바꿔가며 실험 (연습 포인트!)
    print("\n[C 값(정규화 강도)에 따른 정확도 비교]")
    for c in [0.01, 0.1, 1, 10, 100]:
        model = LogisticRegression(C=c, max_iter=5000, random_state=42)
        model.fit(X_train_scaled, y_train)
        test_acc = accuracy_score(y_test, model.predict(X_test_scaled))
        print(f"  C={c:6} -> test_acc={test_acc:.4f}")

    # 8. ROC curve 시각화
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.figure(figsize=(5, 5))
    plt.plot(fpr, tpr, label=f"Logistic Regression (AUC={auc:.3f})", color="#4C72B0")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random guess")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()
    plt.tight_layout()
    plt.savefig("logistic_roc_curve.png", dpi=150)
    print("\n[+] ROC curve를 logistic_roc_curve.png 로 저장했습니다.")

    # ---------------------------------------------------------
    # 연습해볼 것 (TODO):
    # 1) StandardScaler를 빼고 학습해서 성능이 어떻게 달라지는지 비교해보세요.
    # 2) C 값을 극단적으로 작게(0.001) / 크게(1000) 주고 계수(coef_)가 어떻게 변하는지 보세요.
    # 3) penalty="l1", solver="liblinear" 로 바꿔서 일부 계수가 0이 되는(변수 선택) 걸 확인해보세요.
    # 4) threshold(기본 0.5)를 바꿔가며 confusion matrix가 어떻게 달라지는지 실험해보세요.
    # ---------------------------------------------------------


if __name__ == "__main__":
    main()
