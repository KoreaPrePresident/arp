"""
1_decision_tree_practice.py

scikit-learn의 DecisionTreeClassifier 연습용 스크립트.
와인(wine) 데이터셋을 사용해 와인의 화학 성분으로 품종(class)을 분류합니다.

배울 수 있는 것:
- train/test 분리
- 모델 학습 & 예측
- 정확도 / classification_report / confusion_matrix
- feature_importances_ (어떤 특성이 분류에 중요한지)
- max_depth 를 바꿔가며 과적합(overfitting) 관찰
- 트리 시각화
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def main():
    # 1. 데이터 불러오기
    data = load_wine()
    X, y = data.data, data.target
    feature_names = data.feature_names
    class_names = data.target_names

    print(f"[데이터] 샘플 수: {X.shape[0]}, 특성 수: {X.shape[1]}, 클래스: {list(class_names)}\n")

    # 2. train/test 분리 (80% 학습, 20% 테스트)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. 모델 학습 (max_depth를 제한하지 않은 기본 트리)
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[기본 모델] 테스트 정확도: {acc:.4f}\n")
    print("[classification_report]")
    print(classification_report(y_test, y_pred, target_names=class_names))

    print("[confusion_matrix]")
    print(confusion_matrix(y_test, y_pred), "\n")

    # 4. 특성 중요도 (feature_importances_) - 어떤 화학 성분이 분류에 큰 영향을 주는지
    importances = clf.feature_importances_
    top_idx = importances.argsort()[::-1][:5]
    print("[특성 중요도 Top 5]")
    for i in top_idx:
        print(f"  {feature_names[i]:25s} : {importances[i]:.4f}")

    # 5. max_depth를 바꿔가며 과적합 관찰 (연습 포인트!)
    print("\n[max_depth 별 train/test 정확도 비교]")
    depths = [1, 2, 3, 4, 5, None]
    for d in depths:
        model = DecisionTreeClassifier(max_depth=d, random_state=42)
        model.fit(X_train, y_train)
        train_acc = accuracy_score(y_train, model.predict(X_train))
        test_acc = accuracy_score(y_test, model.predict(X_test))
        print(f"  max_depth={str(d):5s} -> train_acc={train_acc:.3f}, test_acc={test_acc:.3f}")

    # 6. 트리 구조 시각화 (max_depth=3으로 제한해서 보기 쉽게)
    simple_tree = DecisionTreeClassifier(max_depth=3, random_state=42)
    simple_tree.fit(X_train, y_train)

    plt.figure(figsize=(16, 8))
    plot_tree(
        simple_tree,
        feature_names=feature_names,
        class_names=class_names,
        filled=True,
        rounded=True,
        fontsize=9,
    )
    plt.title("Decision Tree (max_depth=3)")
    plt.tight_layout()
    plt.savefig("decision_tree.png", dpi=150)
    print("\n[+] 트리 시각화를 decision_tree.png 로 저장했습니다.")

    # ---------------------------------------------------------
    # 연습해볼 것 (TODO):
    # 1) max_depth 값을 바꿔서 train_acc와 test_acc 차이(과적합)를 직접 관찰해보세요.
    # 2) criterion 파라미터를 "gini" -> "entropy" 로 바꿔서 결과가 달라지는지 확인해보세요.
    # 3) load_wine() 대신 load_breast_cancer() 를 사용해 이진 분류로 연습해보세요.
    # 4) GridSearchCV로 max_depth, min_samples_split을 자동 튜닝해보세요.
    # ---------------------------------------------------------


if __name__ == "__main__":
    main()
