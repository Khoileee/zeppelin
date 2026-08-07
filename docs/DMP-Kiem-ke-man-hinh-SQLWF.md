# Kiểm kê màn hình SQLWF — đọc từ mã nguồn
### Tài liệu nền cho Đề xuất tool Data Management

| | |
|---|---|
| **Mục đích** | Xác định **chính xác** SQLWF đang có gì, trước khi đề xuất tool mới — thay cho việc suy đoán theo tên thư mục |
| **Cách làm** | Rút trích tự động từ `sqlwf-fe/src/app`: route · tên control trong form · tiêu đề cột bảng · nhãn nút · lời gọi service. Sau đó đọc tay các chỗ quan trọng |
| **Nguồn** | `app-routing.module.ts` (**120 route**) · 67 thư mục màn hình trong `views/management/` |
| **Ngày** | 04/08/2026 |
| **Trạng thái** | ✅ Đã kiểm kê **19 màn cốt lõi** + entity dữ liệu mức cột + cơ chế OPA · ⏳ Còn 10 màn phụ chưa kiểm kê (mục 5) · ✅ **4/5 câu hỏi đã đóng** |

---

## 1. ⚠️ Chín chỗ tôi đã kết luận SAI trong các tài liệu trước

<details open>
<summary><b>Đọc mục này trước — nó sửa lại phần "SQLWF còn thiếu gì"</b></summary>

| # | Tôi từng viết | Thực tế trong code | Bằng chứng |
|:---:|---|---|---|
| **1** | *"Từ điển nghiệp vụ chưa gắn được vào cột"* | 🔴 **SAI.** Bảng khai trường trong Quản lý bảng **đã có cột `Glossary term`**, và màn gọi `dataGlossaryService.getDataGlossaryByName`. Bản thân Glossary cũng có khối **"Danh sách bảng dữ liệu liên quan"** | `table-management` · `data-glossary` |
| **2** | *"Chưa có nhãn phân loại mức cột"* | 🔴 **SAI HOÀN TOÀN.** Entity `Field` có trường **`tagIds`** ở mức cột, với 3 nhãn chuẩn **`PD_BASIC` · `PD_SENSITIVE` · `DATA_GENERAL`**, mặc định `DATA_GENERAL`. Và nhãn này **được đồng bộ sang OPA** để thực thi phân quyền. Xem [mục 2b](#2b--phát-hiện-quan-trọng-nhất--cấu-trúc-dữ-liệu-ở-mức-cột) | `Field.java` · `TableServiceImpl` |
| **3** | *"Chưa có BDA / DE phụ trách"* | 🔴 **SAI.** Form khai bảng có sẵn 2 trường `businessOwner` và `dataEngineerOwner`. Màn metadata theo domain cũng hiển thị cột **"BDA phụ trách"** và **"DE phụ trách"** | `table-management` · `domain-management` |
| **4** | *"Chưa có chu kỳ cập nhật cam kết"* | 🔴 **SAI.** Form khai bảng có `syncFrequency` và `syncFrequencyOther` | `table-management` |
| **5** | *"Thiếu nơi quản lý mẫu nạp dữ liệu"* | 🔴 **SAI.** Có hẳn màn **Template** với đầy đủ tạo · sửa · bật/tắt · tải file mẫu · gắn vào menu chức năng | `import-data/template` |
| **6** | *"Cần xây mới Thư viện luật (Rule Library)"* | 🟠 **Phải xem lại.** Module **`DMP/warning-rule`** đã là một bộ máy luật: mã cảnh báo · tên rule · loại cảnh báo · **loại so sánh** · **ngưỡng** · nhóm · trung tâm nhận · thời gian áp dụng · **và có quy trình duyệt** (`approveRule` / `rejectRule` / `cancelRule`) | `DMP/warning-rule` |
| **7** | *"Chưa có quy trình duyệt"* | 🔴 **SAI HOÀN TOÀN.** SQLWF có quy trình duyệt ở **ít nhất 4 chỗ**: Glossary (`approveRejectGlossary`) · Job (`requestApproval`/`approve`/`reject`) · Đồng bộ nguồn (`approveRecord`/`rejectRecord`) · Luật cảnh báo (`approveRule`/`rejectRule`) | 4 module |
| **8** | *"Quản lý danh mục ≈ `business-management/profession`"* | 🔴 **SAI.** Quản lý danh mục là **`channel-indexing-management`** — và nó **đã có đủ phê duyệt · phiên bản · so sánh thay đổi · nạp file · xuất Excel · tự sinh menu**. Xem [mục 2c](#2c-quản-lý-danh-mục--codechannel-indexing-managementcode) | `channel-indexing-management` |
| **9** | *"Cần xây mới menu Danh mục tham chiếu (Master Data)"* | 🔴 **SAI.** Chính là màn ở dòng trên. Việc cần làm chỉ là **nối nó vào luật chất lượng** | `channel-indexing-management` |

> **Hệ quả:** phần "SQLWF còn thiếu gì" trong các tài liệu trước **hẹp hơn tôi tưởng khá nhiều**. Nhiều thứ tôi định đề xuất "xây mới" thì thực ra đã có, chỉ **chưa nối với nhau và chưa dùng tới**.

</details>

---

## 2. Kiểm kê chi tiết từng màn

<details open>
<summary><b>① Quản lý bảng — <code>table-management</code></b></summary>

| | |
|---|---|
| **Route** | `table-management` · `create-table` · `edit-table/:id` · `detail-table/:id` |
| **Thư mục con** | `create-table` · `detail-table` · **`upload-management`** |

**Trường trong form khai bảng** *(lấy từ FormGroup)*

| Nhóm | Trường |
|---|---|
| Định danh | `name` · `description` · `type` · `schema` · `path` · `area` · `clusters` · `dataMart` |
| Trách nhiệm | **`businessOwner`** · **`dataEngineerOwner`** · `domainIds` · `subDomainIds` · `createdUsers` |
| Cấu hình ghi | `mode` · `partition` · `partitionBy` · `mergeBy` · `orderBy` · `groupBy` · `delimiter` · `header` · `inferSchema` |
| Đồng bộ | **`syncFrequency`** · `syncFrequencyOther` |
| Chất lượng | `dqEnable` · `dqCycleType` · `dqOffset` · `dqDelay` · `dqComparedCycle` · `metrics` |
| Khác | `businessLink` · `jobName` · `query` · `queryName` · `recordNumber` · `totalSize` · `status` |

**Cột trong bảng khai TRƯỜNG dữ liệu** — đây là chỗ đáng chú ý nhất:

`Tên trường` · `Kiểu dữ liệu` · `Mô tả` · **`Glossary term`** · **`Phân loại dữ liệu`** · **`Quy tắc nghiệp vụ`** · **`Tập giá trị/Khoảng`** · `Khóa chính/Khóa phụ` · `NULLABLE` · `Thuộc tính metadata` · `Tên use case` · `Mô tả use case`

**Hành động** — `createTable` · `updateTable` · `updateSchema` · `previewSchema` · `refreshDataSample` · `getListDataSample` · `getTableDataSummary` · `downloadSchema` · `downloadMetadata` · `downloadTemplate` · `uploadBusinessMetadataFile` · `downloadBusinessMetadataFile` · `searchFileUpload` · `cancelFileUpload` · `downloadFileError`

> 💡 **Nhận xét:** đây đã gần như là một **màn Catalog đầy đủ**. Có mô tả cột, thuật ngữ, phân loại, quy tắc nghiệp vụ, tập giá trị hợp lệ, dữ liệu mẫu, tải lên/xuống metadata nghiệp vụ. Và **"Quản lý upload" là một phần của màn này**, không phải màn riêng.

</details>

<details open>
<summary><b>② Từ điển nghiệp vụ — <code>data-glossary</code></b></summary>

| | |
|---|---|
| **Route** | `data-glossary` · `detail/:id` |
| **Thư mục con** | `create-edit-dialog` · `detail` · `document-management` |

**Trường:** `code` · `name` · `alias` · `definition` · `description` · **`cde`** *(Critical Data Element)* · `owner` · **`stewards`** · **`approveStaffs`** · **`relates`** · **`parent`** · `attachments` · `status` · `reason`

**Hành động:** tạo · sửa · xoá · **duyệt/từ chối** (`approveRejectGlossary`) · tải mẫu · tải lên hàng loạt (`uploadGlossary`) · đính kèm tài liệu · tìm phòng ban · tìm steward · **`searchTable`**

**Khối hiển thị:** *"Danh sách bảng dữ liệu liên quan"*

> 💡 Bộ trường này **đầy đủ hơn mặt bằng thị trường**: có cờ CDE, có steward tách khỏi owner, có người duyệt, có thuật ngữ cha (phân cấp), có thuật ngữ liên quan, có đính kèm tài liệu, có quy trình duyệt.

</details>

<details open>
<summary><b>③ Từ điển đặc trưng — <code>data-dictionary</code></b></summary>

| | |
|---|---|
| **Thư mục con** | `data-dictionary-domain` · `data-dictionary-feature` · `data-dictionary-feedback` · `data-dictionary-version` |

**Trường:** `tableId` · `featureName` · `meaning` · `dataType` · `dataFormat` · `availableValue` · `featureType` · `featureLevel` · `frequency` · `dynamicTimeRange` · `statisticalMetrics` · `dataSource` · `jobName` · `nodeName` · `sampleSize` · `nullValue` · `zeroValue` · `duplicateRow` · `duplicateColumn` · `minValue` · `maxValue` · `meanValue` · `domainGroupId` · `domainProductId`

**Cột bảng:** `DOMAIN_GROUP` · `DOMAIN_GROUP_PRODUCT` · `TABLE_NAME` · `FEATURE_NAME` · `MEANING` · `FREQUENCY`

**Có thêm:** quản lý **phiên bản** · **góp ý** (loại: Bug / Data issue / Suggestion) · tải lên/xuất hàng loạt · cây domain 2 chiều (theo nguồn dữ liệu và theo sản phẩm)

> ⚠️ **Trùng lặp cần xử lý:** các trường `nullValue` · `minValue` · `maxValue` · `meanValue` · `duplicateRow` · `sampleSize` **trùng với chỉ số Profiling** của module Chất lượng. Phải chốt ai đo, ai hiển thị.

</details>

<details open>
<summary><b>④ Chất lượng dữ liệu — <code>data-quality</code></b></summary>

| | |
|---|---|
| **Route** | `data-quality` · `detail/:id` · `download/data-quality` |
| **Thư mục con** | `detail-table` · `notify-manager` |

**Trường:** `dqEnable` · `dqCycleType` · `dqOffset` · `dqDelay` · `dqComparedCycle` · `metrics` · `emailChips` · `isActive`

**Hành động:** `getMetricInfo` · `getDetailDq` · `postDetailDq` · `uploadSetting` · `downloadTemplateSetting` · `refreshDataSample` · `getTableDataSummary` · nhóm nhận cảnh báo (`createDqNotify` · `createDqOwnerNotify` · `getAllDqOwnerNotifyGroup` · `searchNotifyGroup`)

> 💡 Đúng như đã biết: DQ hiện tại = **bật/tắt + chọn chỉ số + đặt chu kỳ + chọn nhóm nhận email**. Chưa có luật nghiệp vụ, chưa có kết quả dạng bảng điều khiển, chưa có sự cố có vòng đời.

</details>

<details open>
<summary><b>⑤ Luật & Hệ thống cảnh báo — <code>DMP/warning-rule</code> + <code>DMP/warning-system</code></b></summary>

| | |
|---|---|
| **Route** | `dmp` · `warning-rule` · `warning-system` |

**Trường:** `code` · `ruleName` · `ruleType` · **`comparisonType`** · **`threshold`** · `warningTimes` · `fromTime` · `toTime` · `group` · `receiverCenters` · `SOC` · `status` · `description`

**Cột bảng cảnh báo:** `Mã cảnh báo` · `Tên rule cảnh báo` · `Loại cảnh báo` · `Loại so sánh` · `Ngưỡng` · **`Giá trị hiện tại`** · **`Thời gian phát hiện`** · `Người tác động` · `Trạng thái`

**Hành động:** `createRule` · `updateRule` · `searchRule` · `getDetailRule` · `getRuleGroup` · **`approveRule`** · **`rejectRule`** · **`cancelRule`** · `searchWarning` · `getWarningDetail` · `changeStatusWarning`

> ⚠️ **Đây là phát hiện quan trọng nhất của đợt kiểm kê.** SQLWF đã có sẵn một **bộ máy luật + cảnh báo có quy trình duyệt**. Trước khi xây "Rule Library" mới cho module Chất lượng, **bắt buộc phải làm rõ module này đang làm gì** — rất có thể chỉ cần mở rộng nó.

</details>

<details open>
<summary><b>⑥ Quản lý Job — <code>job-management</code></b></summary>

| | |
|---|---|
| **Route** | `job-management` · `job-configuration` · `job-update/:id` · `job-clone/:id` |
| **Thư mục con** | `job-list` · `job-configuration` · `job-detail` · `job-step` · `step-diagram` · `sql-viewer` · `job-approval` · `job-save-commit` · `job-tuning-confirm` · `job-tuning-review` · **`job-version-history`** · **`job-version-conflict`** |

**Trường:** `jobName` · `description` · `group` · `outputTable` · `cronExpression` · `coordinatorCode` · **`enableDataLineage`** · `notificationType` · `userGetAlert` · `active` · `status` · `approvedUser` · `approvedDate` · `note`

**Hành động:** tạo · sửa · nhân bản · **xin duyệt / duyệt / từ chối** · **khoá phiên chỉnh sửa** (`acquireLock` · `refreshLock` · `releaseLock`) · **chế độ test** (`updateTestMode`) · **bật quét lineage** (`enableDataLineage`)

> 💡 Mạnh hơn tôi tưởng nhiều: có **lịch sử phiên bản**, **xử lý xung đột khi 2 người sửa cùng lúc**, **khoá phiên**, **sơ đồ bước**, **chế độ chạy thử**, **quy trình duyệt**.

</details>

<details open>
<summary><b>⑦ Nạp dữ liệu — <code>import-data</code></b></summary>

| | |
|---|---|
| **Route** | `upload-data-management` · `template` |
| **Thư mục con** | `template` · `upload-list` · `upload-CTKM` |

**Trường mẫu nạp:** `templateName` · `fileCode` · `fileType` · `encodingType` · `delimiter` · `partitionBy` · `dataCategory` · `dataRange` · **`functionName`** *(gắn vào menu chức năng nào)* · `status`

**Trường lần nạp:** `fileName` · `uploadAt` · `uploadedBy` · `processingStatus` · `tableName` · `range`

**Hành động:** quản lý mẫu (tạo · sửa · bật/tắt · tải file mẫu · lấy danh sách menu) · quản lý lần nạp (tạo · tìm · cập nhật · đổi trạng thái · nạp/tải file tài chính)

> 💡 **Quản lý mẫu nạp đã có sẵn** — tôi từng đề xuất "thiếu tab Mẫu nạp", sai.

</details>

<details open>
<summary><b>⑧ Đồng bộ nguồn — <code>sync-management</code></b></summary>

| | |
|---|---|
| **Thư mục con** | `detail-table` · `sync-tab-panel` |
| **Nguồn hỗ trợ** | **MariaDB · MongoDB · OracleDB** |

**Hành động:** `createRecord` · `updateRecord` · `deleteRecord` · **`approveRecord`** · **`rejectRecord`** · `getDetailRecord` · `listAllClusters`

**Đáng chú ý:** màn này **dùng lại `dqService`** — tức là cấu hình đồng bộ **có kèm luôn cấu hình chất lượng** (`dqEnable`, `dqCycleType`, `dqOffset`, `dqDelay`, `dqComparedCycle`).

> 💡 Đây là một dạng **cổng chất lượng tại cửa nạp** đã manh nha có sẵn.

</details>

<details open>
<summary><b>⑨ Biến đổi dữ liệu — <code>data-transform</code></b></summary>

| | |
|---|---|
| **Route** | `data-transform` · `jdbc-db` · `kafka-topics` |

**Cột cấu hình trường:** `Field Name` · `Type name` · `Format` · **`Precision`** · **`Scale`** · **`Primary key`** · **`Family`** *(HBase)* · **`Bắt buộc`** · `Minimum size` · `Source name` · `Output` · `Process`

**Hành động:** tạo/sửa/bật-tắt luồng · tạo/sửa database JDBC · tạo/sửa Kafka topic

> 💡 Có **ánh xạ schema mức trường** khá chi tiết — bao gồm cả kiểu, độ chính xác, khoá chính, cột bắt buộc.

</details>

<details open>
<summary><b>⑩ Các màn còn lại đã kiểm kê</b></summary>

| Màn | Nội dung chính |
|---|---|
| **`table-monitor`** | Nhóm bảng: `name` · `description` · `path` · `creator` · `status`. Có **bật/tắt từng bảng trong nhóm** (`toggleStatus`), chọn "Các bảng sẵn có → Các bảng được truy cập" |
| **`domain-management`** | Route `metadata/domain/:domainName`. Có `domain-categories` và `domain-details`. Cột hiển thị: **BDA phụ trách · DE phụ trách · Tags · Tên bảng · Hoạt động** |
| **`data-linage`** | Chỉ có 3 lời gọi: `getDetailNodeTable` · `getDetailEdge` · `getExpandLineage`. **Không có form, không có CRUD** — thuần xem |
| **`history-data`** | Nhật ký thay đổi cấu hình: `Đối tượng` · `Loại đối tượng` · `Loại thay đổi` · **`Giá trị cũ`** · **`Giá trị mới`** · `Người thay đổi` · **`IP Address`** · `Thời gian` |
| **`task-management`** | Tác vụ định kỳ: `taskCode` · `programCode` · `cronExpression` · `cycleCode` · `cyclePattern` · `scheduleType` · `inputType` · `parameters` · `ignoreLines`. Có **kết quả lần chạy gần nhất** |
| **`warning-history`** | Lịch sử cảnh báo: `warningCode` · **`incidentCode`** · `taskCode` · `emailReceiver` · `approvalState` · **`isSendTicket`**. Có **duyệt cảnh báo hàng loạt** và **tạo ticket SOC** |
| **`data-authorize`** | Nhóm dữ liệu: `data_authorize_code` · `data_authorize_name` · `status`. Gắn với **thư mục** (`findFoldersByDataAuthorizeId`) |
| **`group-authorize`** | Nhóm quyền: `group_authorize_code` · `group_authorize_name`. Gắn với **menu** (`updateMenuItemsGroup`) |
| **`tags`** | Chỉ 3 trường: `tagName` · `description` · `createdUsers`. **Là nhãn gắn cho người dùng**, không phải nhãn dữ liệu |
| **`file-view-group`** | Quyền thư mục HDFS: `Owner` · `Group` · **`Read` / `Write` / `Execute`** · **`Encrypted`** · **`Erasure Coding`** · **`Apply all children`** |
| **`invoice-uploader`** | Nạp hoá đơn, có **"Kết quả team AI xử lý"** |
| **`acl`** | Ma trận **Menu chức năng × Quyền/component** |
| **`connection-management`** | Kết nối nguồn rất đầy đủ: `connectionType` · `databaseType` · `databaseConnectionURL` · `databaseConnectionIpList` · `ftpIpAddress` · `kafkaBrokers` · `topics` · **`keberos`** · **`keytab`** · **`principal`** · `protocol` · `portCLI` · `portData` |
| **`configuration-management`** | Cấu hình theo `taskCode`, có **Source name → Target name → Target type → Order**, và **nhật ký cấu hình** (`detail-log-configuration`) |

**⚠️ Phát hiện quan trọng ở `user-managerment`** — các cột trên màn phân quyền người dùng:

`Phân quyền truy cập dữ liệu` · `Phân quyền File View` · **`Phân quyền danh mục`** · `Phân quyền PYC` · **`Tên danh mục`** · **`Tên tags phân loại dữ liệu`** · `Duyệt dữ liệu` · `Thao tác dữ liệu` · `Cho phép truy cập`

> 💡 Hai điều rút ra:
> 1. **"Danh mục" là một đối tượng có thật và có phân quyền riêng** → câu hỏi **H4** đã có manh mối, cần hỏi dev xem màn quản lý nó nằm ở đâu.
> 2. **"Tags phân loại dữ liệu" đã tồn tại** như một khái niệm gắn với người dùng → củng cố nghi ngờ ở **H2**: phần nền của Classification có thể đã có, chỉ chưa dùng để áp chính sách.

</details>

---

## 2b. ⭐ Phát hiện quan trọng nhất — cấu trúc dữ liệu ở MỨC CỘT

<details open>
<summary><b>Entity <code>Field</code> — SQLWF đã quản lý rất nhiều thứ ở mức cột</b></summary>

Đọc `sqlwf-be/.../entity/mongo/object/Field.java` — mỗi **cột** của một bảng đang lưu:

| Trường | Ý nghĩa | Ghi chú |
|---|---|---|
| `name` · `type` · `description` | Tên · kiểu · mô tả | |
| **`glossaryTeam`** | **Thuật ngữ nghiệp vụ gắn vào cột** | ✅ Liên kết Glossary ↔ Cột **đã tồn tại ở tầng dữ liệu** |
| **`tagIds`** | **Nhãn phân loại dữ liệu của cột** | ✅ `PD_BASIC` · `PD_SENSITIVE` · `DATA_GENERAL`, mặc định `DATA_GENERAL` |
| **`metrics`** | Danh sách chỉ số chất lượng của cột | Mỗi chỉ số có `dimension` · `dqType` · `dqMin` · `dqMax` · `dqEnum` · **`dqExpr`** |
| **`dqType` · `dqMin` · `dqMax` · `dqEnum`** | Luật chất lượng ngay trên cột | **`dqEnum` = tập giá trị hợp lệ** · `dqMin`/`dqMax` = khoảng cho phép |
| `isKey` · `keyType` · `nullable` | Khoá chính/phụ · cho phép rỗng | |
| `valueRange` · `businessRule` | Tập giá trị/khoảng · quy tắc nghiệp vụ | Dạng chữ, người dùng tự mô tả |
| `dateFormat` · `codecable` · `order` | Định dạng ngày · mã hoá được · thứ tự | |

**Chuỗi phân quyền theo nhãn đã chạy thật:**

```
Cột có tagIds  ──►  TableServiceImpl.SyncTableTagIds()  ──►  đẩy sang OPA
                                                              ▲
Người dùng được gán tag ở màn "Phân quyền truy cập dữ liệu" ──┘
```

`SyncTableTagIds(tableName)` gọi `POST {endpointOPABase}{endpointOPATableSync}{tableName}` mỗi khi cập nhật bảng.

> 🔴 **Ba kết luận trước đây của tôi bị lật ngược:**
>
> 1. *"Chưa có nhãn phân loại mức cột"* → **SAI.** Có `tagIds` ở mức cột, có 3 nhãn chuẩn, có đồng bộ sang OPA.
> 2. *"Chưa có chính sách theo nhãn"* → **SAI.** Chuỗi cột-có-nhãn → OPA → người-dùng-có-nhãn **đã tồn tại**.
> 3. *"Chưa có luật chất lượng ở mức cột"* → **SAI một phần.** `dqEnum` (tập giá trị hợp lệ), `dqMin`/`dqMax` (khoảng), `dqExpr` (biểu thức) **đã có sẵn trong lược đồ**.
>
> **Việc phải làm không phải xây mới, mà là:** *(a)* làm rõ OPA đang thực thi tới mức nào — chặn cả bảng hay ẩn từng cột; *(b)* xác minh `dqEnum`/`dqExpr` đã dùng thật chưa hay chỉ khai mà không chạy.

</details>

---

## 2c. Quản lý danh mục — <code>channel-indexing-management</code>

<details open>
<summary><b>Đã xác định được (câu hỏi H4 đóng lại) — và nó đầy đủ hơn tôi hình dung</b></summary>

| | |
|---|---|
| **Đường dẫn** | `/#/channel-indexing-management` · `channel-indexing-categories` · `/channel-indexing/:schemaName` |
| **Thư mục con** | `channel-indexing-categories` · `channel-indexing-details` |

**Mô hình 2 tầng**

| Tầng | Nội dung |
|---|---|
| **Tầng 1 — Định nghĩa danh mục** | `schemaName` · `schemaDisplayName` · `Tên nhóm danh mục` · `Tên nhóm danh mục cha` · `status`. Mỗi danh mục khai các trường: **Tên trường · Kiểu dữ liệu · Định dạng · Min · Max · Bắt buộc · Primary key · Alias · Mô tả · Mục đích sử dụng** |
| **Tầng 2 — Dữ liệu trong danh mục** | Từng bản ghi, có `ID bản ghi` · `Version` · `Trạng thái` |

**Những thứ đã có sẵn — đáng chú ý**

| Tính năng | Bằng chứng |
|---|---|
| **Quy trình phê duyệt bản ghi** | Cột `Cần phê duyệt` · `changeApproveStatusData` |
| **Phiên bản + so sánh phiên bản** | `getAllLogVersionBySchemaName` · `getLogVersionBySchemaNameAndVersion` · `compareDataVersion`; cột `Giá trị cũ` · `Giá trị mới` · `Loại thay đổi` · `Lý do thay đổi` · `Người thực hiện` · `Ngày thực hiện` |
| **Nạp hàng loạt từ file** | `uploadFileData` · `processDataFile` |
| **Xuất Excel** | `exportFileExcel` |
| **Tự sinh menu cho từng danh mục** | `menuService.createMenu` · `getDsdmMenuInfo` · `changeMenuStatus` · `getAllGroupMenuItem` |
| **Bật/tắt từng danh mục** | `toggleTable` · hộp thoại *"Xác nhận bật/tắt danh mục"* |

> 💡 **Đây chính là module Master Data mà tôi định đề xuất "xây mới" ở menu 1.4 — hoá ra đã có, và còn có cả phê duyệt, phiên bản, so sánh thay đổi.**
>
> Việc cần làm chỉ còn: **nối nó vào luật chất lượng** để luật *"mã đối tác phải tồn tại trong danh mục"* chạy được — hiện danh mục và chất lượng chưa biết đến nhau.

</details>

---

## 2d. OPA đang thực thi cái gì — đã truy ra từ cấu hình

<details open>
<summary><b>Câu hỏi H2 — trả lời được một nửa từ code, nửa còn lại nằm ngoài repo</b></summary>

**Cấu hình thật trong `application.properties`:**

```properties
opa-collector.base=http://10.58.244.169:9123
opa-collector.sync-blacklist.table.endpoint=/api/table/sync/
opa-collector.sync-blacklist.username.endpoint=/api/function/sync/username/
opa-collector.sync-blacklist.tagId.endpoint=/api/function/sync/tag/
```

**SQLWF đẩy sang OPA 3 loại dữ liệu:**

| Đẩy cái gì | Từ đâu | Khi nào |
|---|---|---|
| Bảng → cột → `tagIds` | `TableServiceImpl.SyncTableTagIds()` | Mỗi lần cập nhật bảng |
| Người dùng → nhãn | `TagServiceImpl` | Khi gán nhãn cho người dùng |
| Nhãn → **danh sách hàm SQL bị cấm** | `FunctionServiceImpl.assignFunctionBlackList()` | Khi cấu hình chặn hàm |

**Kết luận rút ra từ tên gọi trong code** — toàn bộ nhóm này tên là **`sync-blacklist`**, entity là **`TagFunctionBlacklist`**, kho là **`TagFunctionBlackListRepository`**:

> 🔎 **Cơ chế hiện tại là CHẶN HÀM SQL theo nhãn (Query Guard), KHÔNG phải che dữ liệu.**
>
> Không tồn tại bất kỳ trường nào kiểu `maskType` / `maskOption` / `rowFilter` trong toàn bộ mã nguồn — trong khi che dữ liệu bắt buộc phải có *(cột nào, nhóm nào, che kiểu gì)*.

**Phần chưa trả lời được:** luật thực thi cuối cùng nằm trong **OPA Collector** — một service riêng ở `10.58.244.169:9123`, **không có mã nguồn trong workspace này**. Muốn biết chính xác người thiếu nhãn `PD_SENSITIVE` thì bị chặn cả bảng hay chỉ chặn vài hàm, phải xem repo của OPA Collector.

**Ảnh hưởng tới đề xuất:**

| | Kết luận |
|---|---|
| Che dữ liệu (masking) | 🔴 **Vẫn phải xây mới** — không có dấu vết nào |
| Nhưng nền móng | 🟢 **Đã có**: nhãn ở mức cột · người dùng có nhãn · đường đồng bộ sang OPA đã chạy. **Không phải bắt đầu từ số 0** |

</details>

---

## 3. Sau kiểm kê — SQLWF thực sự còn thiếu gì

<details open>
<summary><b>Danh sách rút gọn lại, chỉ giữ những thứ CHẮC CHẮN thiếu</b></summary>

| # | Thiếu thật | Vì sao chắc chắn |
|:---:|---|---|
| **T1** | **Che dữ liệu theo cột (masking)** | Không có bất kỳ service/trường nào liên quan trong toàn bộ mã FE |
| **T2** | **Lọc theo dòng (row-level filter)** | Tương tự |
| **T3** | **Che dữ liệu ở mức cột (masking)** | ✅ **Đã truy ra:** cơ chế OPA hiện tại tên là **`sync-blacklist`**, entity là **`TagFunctionBlacklist`** → bản chất là **chặn hàm SQL theo nhãn**, không phải che dữ liệu. **Không tồn tại** trường `maskType`/`maskOption`/`rowFilter` nào trong mã nguồn.<br>→ **Phải xây mới**, nhưng nền móng (nhãn mức cột · người dùng có nhãn · đường đồng bộ OPA) **đã có**. Chi tiết ở [mục 2d](#2d-opa-đang-thực-thi-cái-gì--đã-truy-ra-từ-cấu-hình) |
| **T4** | **Nguồn gốc mức CỘT + màn phân tích ảnh hưởng** | `data-linage` chỉ có 3 lời gọi xem đồ thị, không có phân tích ảnh hưởng, không xuất danh sách |
| **T5** | **Tìm kiếm toàn văn** (theo tên cột, mô tả, thuật ngữ) | `searchTable` chỉ nhận `tableName` |
| **T6** | **Toàn bộ phần luật chất lượng phải làm lại** | ✅ **Đã có câu trả lời:** tính năng chất lượng mức cột **đã hỏng và bị bỏ từ lâu**, không ai rõ còn chạy được không.<br>→ Lược đồ dữ liệu (`dqType` · `dqMin` · `dqMax` · `dqEnum` · `dqExpr` · `MetricInfo.dimension`) **vẫn dùng lại được**, nhưng **phần chạy coi như phải làm mới**. Cộng thêm hai loại còn thiếu hẳn: **regex định dạng** và **tham chiếu sang bảng danh mục** |
| **T7** | **Sự cố chất lượng có vòng đời và người xử lý** | `warning-history` có duyệt và tạo ticket SOC, nhưng **không có trạng thái Mới → Đang xử lý → Đã đóng**, không có người được gán |
| **T8** | **Bảng điều khiển chất lượng toàn cảnh + điểm chất lượng** | Không có màn nào tổng hợp |
| **T9** | **Báo cáo "một người đang có quyền gì"** | Quyền rải ở `data-authorize`, `group-authorize`, `file-view-group`, `feature-menu-authorization` — không có nơi tổng hợp |
| **T10** | **Lưu mẫu dòng dữ liệu sai** khi luật thất bại | Không có trường nào lưu mẫu dòng lỗi |

**Và những thứ ĐÃ CÓ nhưng chưa nối với nhau** — đây mới là phần lớn công việc:

| Đã có ở đâu | Chưa nối vào đâu |
|---|---|
| `glossaryTeam` trên từng cột | Chưa dùng để tìm kiếm |
| `tagIds` trên từng cột + đồng bộ OPA | ⚠️ Chưa rõ OPA thực thi tới mức nào — **câu hỏi H2 mới** |
| `dqEnum` · `dqMin` · `dqMax` · `dqExpr` trên từng cột | Chưa rõ có được đem đi chạy kiểm tra không |
| `valueRange` · `businessRule` trên từng cột | Đang là chữ tự do, **chưa máy đọc được** để sinh luật |
| **Quản lý danh mục** (`channel-indexing-management`) — có phê duyệt, phiên bản, so sánh thay đổi | **Chưa nối vào luật chất lượng** → luật "mã phải tồn tại trong danh mục" không chạy được |
| Cơ chế **đồng bộ nhãn sang OPA** đã chạy thật | Mới dùng để **chặn hàm SQL**, chưa dùng để **che dữ liệu** |
| Chỉ số thống kê trong `data-dictionary` | Trùng với Profiling của `data-quality`, hai nơi cùng đo |
| `DMP/warning-rule` — bộ máy luật có duyệt | Chưa dùng cho chất lượng dữ liệu |
| `syncFrequency` trong khai bảng | Chưa dùng để cảnh báo dữ liệu trễ |
| `businessOwner` / `dataEngineerOwner` | Chưa dùng để gán sự cố |
| `enableDataLineage` trên job | Mặc định tắt, không ai bật |

</details>

---

## 4. Trùng lặp phát hiện trong chính SQLWF

<details open>
<summary><b>Năm chỗ SQLWF đang tự trùng với chính mình</b></summary>

| # | Trùng ở đâu | Chi tiết |
|:---:|---|---|
| **1** | **Chỉ số thống kê cột** | `data-dictionary` (`nullValue`, `minValue`, `maxValue`, `meanValue`, `duplicateRow`, `sampleSize`) ↔ `data-quality` (`metrics`, `getTableDataSummary`) |
| **2** | **Mô tả cột** | Bảng khai trường trong `table-management` ↔ `featureName` + `meaning` trong `data-dictionary` |
| **3** | **Cấu hình chất lượng** | `table-management` có `dqEnable`/`dqCycleType`/… ↔ `data-quality` cũng có ↔ `sync-management` cũng dùng lại `dqService` — **ba màn cùng khai một bộ cấu hình** |
| **4** | **Luật + ngưỡng + cảnh báo** | `DMP/warning-rule` ↔ `data-quality/notify-manager` ↔ `warning-history` |
| **5** | **Dữ liệu mẫu** | `tableService.refreshDataSample` ↔ `dqService.refreshDataSample` — hai service khác nhau làm cùng một việc |

> Đây chính là biểu hiện cụ thể của vấn đề **V1 — không có nguồn sự thật duy nhất**, và là lý do mạnh nhất để làm tool tập trung.

</details>

---

## 5. Còn phải kiểm kê và còn phải hỏi

<details open>
<summary><b>Mười màn chưa kiểm kê + tình trạng các câu hỏi</b></summary>

**Chưa kiểm kê** *(nằm trong phạm vi nhưng chưa đọc code)*

`pentaho-job-management` v1/v2 · `data-migration-management` · `clean-delivery` · `fsync` · `user-managerment` · `group-management` · `acl` · `feature-menu-authorization` · `configuration-management` · `connection-management`

**Tình trạng các câu hỏi**

| # | Câu hỏi | Ảnh hưởng tới |
|:---:|---|---|
| ~~**H1**~~ | ~~`DMP/warning-rule` đang làm gì~~ | ✅ **Đóng** — không liên quan tới chất lượng dữ liệu |
| ~~**H2**~~ | ~~OPA thực thi nhãn tới mức nào~~ | ✅ **Đóng ở mức đủ để quyết định** — cơ chế là chặn hàm SQL, không phải che dữ liệu → che dữ liệu phải xây mới. *(Muốn biết chi tiết hơn phải xem repo OPA Collector, nhưng không cần cho việc lập kế hoạch)* |
| ~~**H2b**~~ | ~~Luật chất lượng mức cột có chạy không~~ | ✅ **Đóng** — đã hỏng và bỏ từ lâu, phải làm lại phần chạy |
| ~~**H4**~~ | ~~Quản lý danh mục là màn nào~~ | ✅ **Đóng** — là `channel-indexing-management` |
| **H5** | **Bao nhiêu % job đang bật `enableDataLineage`?** | Câu duy nhất còn treo. Quyết định sơ đồ nguồn gốc hiện tại đáng tin đến đâu |
| **H3** | **`data-dictionary` phục vụ ai?** Các trường `featureType`, `featureLevel`, `frequency`, `dynamicTimeRange` nghe như dành cho chọn đặc trưng mô hình học máy | Quyết định gộp hẳn vào tab Cột hay giữ riêng |
| **H4** | **"Quản lý danh mục" là màn nào?** Tôi vẫn chưa xác định được trong 120 route | Quyết định có cần menu Danh mục tham chiếu không |
| **H5** | **Bao nhiêu % job đang bật `enableDataLineage`?** | Quyết định sơ đồ nguồn gốc hiện tại đáng tin đến đâu |

</details>

---

**Hết tài liệu kiểm kê.** Kết quả này sẽ dùng để viết lại mục 3–4 của [Đề xuất tool Data Management](DMP-De-xuat-tool-Data-Management.md).
