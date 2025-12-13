# COMSOL実装仕様書：指定変位による周期的境界条件 (Manual PBC)

## 1\. 概要

本実装は、COMSOL標準の「周期的境界条件」機能を使用せず、対向面の変位をカップリング演算子で参照し、数式で拘束することで周期性を実現する手法である。
主に**均質化法による弾性定数算出**において、任意の巨視的ひずみモード（$E_{ij}$）を強制的に与えるために使用される。

## 2\. 理論と数式ロジック

### 物理的解釈

対向する2つの面（ソース面とデスティネーション面）に対し、以下の関係を強制する。

> 「デスティネーション面の変形」は、「ソース面の変形」から「巨視的ひずみによる変位差分」を引いたものに等しい。

### 拘束式

デスティネーション面（例：$+X$面）における変位 $u_{dest}$ は以下の式で記述される。

$$u_{dest} = \text{coupleOp}(u_{src}) - E_{ij} \times L \times \text{disp}$$

| 変数/項 | 説明 | 備考 |
| :--- | :--- | :--- |
| **$u_{dest}$** | 現在設定している面の変位 | 指定変位ノードで拘束される値 |
| **$\text{coupleOp}(u_{src})$** | 対向面の変位値 | `coupleX` 等の一般押出演算子で取得 |
| **$E_{ij}$** | 巨視的ひずみテンソル成分 | 入力パラメータ（$E_{11}, E_{12} \dots$） |
| **$L$** | 座標変数（$X, Y, Z$） | セルサイズに相当する長さ |
| **$\text{disp}$** | スケーリング係数 | 微小変形制御やOn/Offスイッチとして利用 |

-----

## 3\. Java API 実装設計 (`ComsolJobManager`)

Javaプログラム側では、X, Y, Z各方向に対してループ処理を行い、効率的にノードを作成する。

### 処理フロー

1.  **Physics作成**: `SolidMechanics` インターフェースを作成。
2.  **剛体拘束**: 不定性排除のため、一点または一面を `Fixed Constraint` で固定。
3.  **周期性ループ**: 3方向（X, Y, Z）に対し、`Displacement2`（指定変位）機能を作成し、上記「拘束式」を適用。

### コードスニペット（中核ロジック）

```java
// 定義済み配列: dispTags, selections, labels, coupleOps, coords, strainParamsを使用

for (int i = 0; i < 3; i++) {
    // 1. 指定変位機能(Face)の作成
    PhysicsFeature disp = model.physics("solid").create(dispTags[i], "Displacement2", 2);
    disp.label(labels[i]);
    
    // 2. 適用面の選択 (事前に定義されたSelectionタグを使用)
    disp.selection().named(selections[i]);
    
    // 3. 全方向(u,v,w)を拘束
    disp.set("Direction", new int[][]{{1}, {1}, {1}});
    
    // 4. 数式の構築: couple(u) - E_comp * Coord * disp
    String op = coupleOps[i];
    String X  = coords[i];
    String[] E = strainParams[i]; // {E11, E21, E31} など
    
    String eqU = String.format("%s(u) - %s * %s * disp", op, E[0], X);
    String eqV = String.format("%s(v) - %s * %s * disp", op, E[1], X);
    String eqW = String.format("%s(w) - %s * %s * disp", op, E[2], X);
    
    // 5. 式のセット
    disp.set("U0", new String[][]{{eqU}, {eqV}, {eqW}});
}
```

-----

## 4\. 必須前提条件 (Prerequisites)

このJavaコードが正しく動作するためには、COMSOLモデル側（mphファイルまたは先行するJavaコード）で以下の定義が完了している必要がある。

### A. Global Parameters (パラメータ)

数式内で参照される変数の定義。

  * `disp`: 変位スケーリング係数（例: `1` または `0.001`）
  * `E11` ～ `E33`: ひずみテンソル成分（解析ケースごとに値を変更）
  * `L_x`, `L_y`, `L_z`: セルサイズ（推奨）

### B. Definitions \> Couplings (一般押出演算子)

対向面の値を参照するためのマッピング定義。最も設定ミスが起きやすい箇所。

| 演算子名 | Source Selection | Destination Map (重要) |
| :--- | :--- | :--- |
| **`coupleX`** | $-X$面 (最小面) | `x - L_x`, `y`, `z` |
| **`coupleY`** | $-Y$面 (最小面) | `x`, `y - L_y`, `z` |
| **`coupleZ`** | $-Z$面 (最小面) | `x`, `y`, `z - L_z` |

### C. Geometry \> Selections (明示的選択)

Javaコードから `named("...")` で呼び出すためのタグ付け。

  * **Dest面**: `geom1_boxsel2` (+X), `geom1_boxsel4` (+Y), `geom1_boxsel6` (+Z)
  * **Fix面/点**: `geom1_boxsel7` (剛体拘束用)
  * **Source面**: 上記Couplings定義用にタグ付けが必要。

-----

## 5\. 実装チェックリスト

`ComsolJobManager` 開発時に以下の項目を確認すること。

  - [ ] **パラメータ注入**: `disp` および `Eij` がモデルにパラメータとして設定されているか？
  - [ ] **演算子生成**: `coupleX`, `coupleY`, `coupleZ` が `GeneralExtrusion` として定義されているか？
  - [ ] **マッピング**: 一般押出の「Destination Map」式で、座標のシフト（`-L_x`等）が正しく記述されているか？
  - [ ] **選択タグ**: ジオメトリ作成時に `boxsel` 等のタグが意図した面（+X面など）に付与されているか？（自動連番に依存する場合は順序に注意）
