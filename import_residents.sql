-- استيراد بيانات السكان
BEGIN;


INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'يحيى بن علي بن يحيى العمري', '1000000001', '504444120',
       (SELECT id FROM buildings WHERE building_number = 'V1' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'يحيى بن علي بن يحيى العمري');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'مشبب بن سعيد بن ظويفر القحطاني', '1000000002', '507665005',
       (SELECT id FROM buildings WHERE building_number = 'V2' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'مشبب بن سعيد بن ظويفر القحطاني');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عمر بن عبدالرحمن بن محمد العمر', '1000000003', '505828583',
       (SELECT id FROM buildings WHERE building_number = 'V3' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عمر بن عبدالرحمن بن محمد العمر');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'يحيى بن صالح بن إبراهيم الطويان', '1000000004', '504205092',
       (SELECT id FROM buildings WHERE building_number = 'V4' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'يحيى بن صالح بن إبراهيم الطويان');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'محمد بن ناجي بن ناصر اليماني', '1000000005', '561144374',
       (SELECT id FROM buildings WHERE building_number = 'V5' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'محمد بن ناجي بن ناصر اليماني');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالرحمن بن محمد بن عبدالرحمن الخراشي', '1000000006', '505233312',
       (SELECT id FROM buildings WHERE building_number = 'V6' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالرحمن بن محمد بن عبدالرحمن الخراشي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالكريم بن عبدالله بن محمد العبدالكريم', '1000000007', '505946304',
       (SELECT id FROM buildings WHERE building_number = 'V7' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالكريم بن عبدالله بن محمد العبدالكريم');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالله بن محمد بن عبدالعزيز المفلح', '1000000008', '500688896',
       (SELECT id FROM buildings WHERE building_number = 'V8' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالله بن محمد بن عبدالعزيز المفلح');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالله بن ثاني بن عامق الرويلي', '1000000009', '556311136',
       (SELECT id FROM buildings WHERE building_number = 'V9' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالله بن ثاني بن عامق الرويلي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'خالد بن عبدالعزيز بن محمد الداود', '1000000010', '555466211',
       (SELECT id FROM buildings WHERE building_number = 'V10' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'خالد بن عبدالعزيز بن محمد الداود');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أحمد بن عبدالله بن أحمد الجميد ((السالم))', '1000000011', '505407387',
       (SELECT id FROM buildings WHERE building_number = 'V11' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أحمد بن عبدالله بن أحمد الجميد ((السالم))');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالحميد بن عبدالله بن ناصر المجلي ', '1000000012', '503116763',
       (SELECT id FROM buildings WHERE building_number = 'V12' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالحميد بن عبدالله بن ناصر المجلي ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'إبراهيم بن عبدالله بن عبدالعزيز السعدان', '1000000013', '555525285',
       (SELECT id FROM buildings WHERE building_number = 'V13' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'إبراهيم بن عبدالله بن عبدالعزيز السعدان');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'محمد بن عبدالعزيز بن محمد أباعود', '1000000014', '504254745',
       (SELECT id FROM buildings WHERE building_number = 'V14' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'محمد بن عبدالعزيز بن محمد أباعود');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'محمد بن عبدالعزيز بن محمد الفيصل', '1000000015', '554447423',
       (SELECT id FROM buildings WHERE building_number = 'V15' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'محمد بن عبدالعزيز بن محمد الفيصل');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'إبراهيم بن زيد بن حمد الفحيلة', '1000000016', '555210570',
       (SELECT id FROM buildings WHERE building_number = 'V16' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'إبراهيم بن زيد بن حمد الفحيلة');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أمل بنت سليمان بن محمد السيف', '1000000017', '546090808',
       (SELECT id FROM buildings WHERE building_number = 'V17' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أمل بنت سليمان بن محمد السيف');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'حياة بنت يوسف بن منصور الصبياني', '1000000018', '503428297',
       (SELECT id FROM buildings WHERE building_number = 'V18' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'حياة بنت يوسف بن منصور الصبياني');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالعزيز بن محمد بن عبدالله السحيباني', '1000000019', '505498660',
       (SELECT id FROM buildings WHERE building_number = 'V19' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالعزيز بن محمد بن عبدالله السحيباني');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'صالح بن فهد بن صالح العصيمي', '1000000020', '505488897',
       (SELECT id FROM buildings WHERE building_number = 'V20' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'صالح بن فهد بن صالح العصيمي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالله بن عبدالرحمن بن عبدالعزيز التريكي', '1000000021', '505267647',
       (SELECT id FROM buildings WHERE building_number = 'V21' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالله بن عبدالرحمن بن عبدالعزيز التريكي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالرحمن بن عبدالله بن عبدالعزيز الخضيري', '1000000022', '505486484',
       (SELECT id FROM buildings WHERE building_number = 'V22' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالرحمن بن عبدالله بن عبدالعزيز الخضيري');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'ضيف الله بن دليم بن فيحان العتيبي', '1000000023', '503138437',
       (SELECT id FROM buildings WHERE building_number = 'V23' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'ضيف الله بن دليم بن فيحان العتيبي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أحمد بن محمد بن محمد النشوان ', '1000000024', '504445574',
       (SELECT id FROM buildings WHERE building_number = 'V24' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أحمد بن محمد بن محمد النشوان ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'وليد بن عبدالعزيز بن سليمان الجندل ', '1000000025', '505473949',
       (SELECT id FROM buildings WHERE building_number = 'V25' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'وليد بن عبدالعزيز بن سليمان الجندل ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'مشعل بن سليمان بن عواد العنزي', '1000000026', '567778911',
       (SELECT id FROM buildings WHERE building_number = 'V26' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'مشعل بن سليمان بن عواد العنزي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالكريم بن عبدالعزيز بن أحمد المحرج', '1000000027', '505783432',
       (SELECT id FROM buildings WHERE building_number = 'V27' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالكريم بن عبدالعزيز بن أحمد المحرج');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'سليمان بن سليمان بن عبد العزيز العنقري ', '1000000028', '505103580',
       (SELECT id FROM buildings WHERE building_number = 'V28' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'سليمان بن سليمان بن عبد العزيز العنقري ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'وعد بنت محمد بن عبدالله الحوشان', '1000000029', '554334240',
       (SELECT id FROM buildings WHERE building_number = 'V29' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'وعد بنت محمد بن عبدالله الحوشان');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالعزيز بن ناصر بن عبدالعزيز التميمي', '1000000030', '555139319',
       (SELECT id FROM buildings WHERE building_number = 'V30' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالعزيز بن ناصر بن عبدالعزيز التميمي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'طلال بن خالد بن حسين الطريفي', '1000000031', '505168786',
       (SELECT id FROM buildings WHERE building_number = 'V31' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'طلال بن خالد بن حسين الطريفي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'باسم بن عبدالله بن صالح الزغيبي', '1000000032', '505257736',
       (SELECT id FROM buildings WHERE building_number = 'V32' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'باسم بن عبدالله بن صالح الزغيبي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'حمد بن ناصر بن عبدالعزيز التريكي', '1000000033', '505242818',
       (SELECT id FROM buildings WHERE building_number = 'V33' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'حمد بن ناصر بن عبدالعزيز التريكي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالله بن محمد بن مبارك الوزرة', '1000000034', '567071111',
       (SELECT id FROM buildings WHERE building_number = 'V34' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالله بن محمد بن مبارك الوزرة');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالرحمن بن عبدالعزيز بن عبدالله المقبل  ', '1000000035', '503447494',
       (SELECT id FROM buildings WHERE building_number = 'V35' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالرحمن بن عبدالعزيز بن عبدالله المقبل  ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عفراء بنت صالح عبدالرحمن الشيبان', '1000000036', '544992533',
       (SELECT id FROM buildings WHERE building_number = 'V36' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عفراء بنت صالح عبدالرحمن الشيبان');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'آمنة بنت محمد بن علي العروي', '1000000037', '551874730',
       (SELECT id FROM buildings WHERE building_number = 'V37' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'آمنة بنت محمد بن علي العروي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'ماجد بن عبدالله بن إبراهيم البصيص', '1000000038', '505298916',
       (SELECT id FROM buildings WHERE building_number = 'V38' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'ماجد بن عبدالله بن إبراهيم البصيص');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'بدر بن محمد بن أحمد عقيلي', '1000000039', '567719955',
       (SELECT id FROM buildings WHERE building_number = 'V39' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'بدر بن محمد بن أحمد عقيلي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالمحسن بن عبدالرزاق بن عبدالرحمن الغديان ', '1000000040', '598163226',
       (SELECT id FROM buildings WHERE building_number = 'V40' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالمحسن بن عبدالرزاق بن عبدالرحمن الغديان ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'صالح بن مده بن حميدان الجدعاني', '1000000041', '554881137',
       (SELECT id FROM buildings WHERE building_number = 'V41' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'صالح بن مده بن حميدان الجدعاني');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'جميل بن عبدالمحسن بن حمد الخلف', '1000000042', '504423913',
       (SELECT id FROM buildings WHERE building_number = 'V42' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'جميل بن عبدالمحسن بن حمد الخلف');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'باسم بن إبراهيم بن سليمان المحيميد', '1000000043', '503100166',
       (SELECT id FROM buildings WHERE building_number = 'V43' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'باسم بن إبراهيم بن سليمان المحيميد');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'ياسر بن إبراهيم بن محمد الخضيري', '1000000044', '502093793',
       (SELECT id FROM buildings WHERE building_number = 'V44' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'ياسر بن إبراهيم بن محمد الخضيري');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'حمد بن منصور بن عبدالله الدوسري', '1000000045', '554245300',
       (SELECT id FROM buildings WHERE building_number = 'V45' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'حمد بن منصور بن عبدالله الدوسري');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عمر بن خالد بن عبدالرحمن الدعيج', '1000000046', '555026260',
       (SELECT id FROM buildings WHERE building_number = 'V46' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عمر بن خالد بن عبدالرحمن الدعيج');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'يوسف بن أحمد يوسف الدريويش', '1000000047', '506030030',
       (SELECT id FROM buildings WHERE building_number = 'V47' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'يوسف بن أحمد يوسف الدريويش');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالحميد بن عبدالله بن محمد المشعل', '1000000048', '504420685',
       (SELECT id FROM buildings WHERE building_number = 'V48' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالحميد بن عبدالله بن محمد المشعل');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أحمد بن ناصر بن عبدالله آل مقبل', '1000000049', '553455155',
       (SELECT id FROM buildings WHERE building_number = 'V49' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أحمد بن ناصر بن عبدالله آل مقبل');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالمحسن بن صالح بن عبدالله الرشودي', '1000000050', '503143500',
       (SELECT id FROM buildings WHERE building_number = 'V50' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالمحسن بن صالح بن عبدالله الرشودي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'إيمان بنت بدر بن عبدالله البدر', '1000000051', '554471817',
       (SELECT id FROM buildings WHERE building_number = 'V51' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'إيمان بنت بدر بن عبدالله البدر');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'بدرية بنت محمد بن عبدالله الوهيبي', '1000000052', '555581117',
       (SELECT id FROM buildings WHERE building_number = 'V52' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'بدرية بنت محمد بن عبدالله الوهيبي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'صالح بن عبدالله بن محمد الصالح', '1000000053', '504434676',
       (SELECT id FROM buildings WHERE building_number = 'V53' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'صالح بن عبدالله بن محمد الصالح');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'فوزية بنت فهد بن علي المسند', '1000000054', '505229006',
       (SELECT id FROM buildings WHERE building_number = 'V54' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'فوزية بنت فهد بن علي المسند');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالعزيز بن ناصر بن عبدالرحمن الخريف', '1000000055', '504453880',
       (SELECT id FROM buildings WHERE building_number = 'V55' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالعزيز بن ناصر بن عبدالرحمن الخريف');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'يوسف بن عبدالرحمن بن يوسف الشبل', '1000000056', '506250100',
       (SELECT id FROM buildings WHERE building_number = 'V56' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'يوسف بن عبدالرحمن بن يوسف الشبل');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالهادي بن شرهان بن عابد العتيبي  ', '1000000057', '554799955',
       (SELECT id FROM buildings WHERE building_number = 'V57' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالهادي بن شرهان بن عابد العتيبي  ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'الجوهرة بنت محمد بن عبدالله العمراني', '1000000058', '504104774',
       (SELECT id FROM buildings WHERE building_number = 'V58' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'الجوهرة بنت محمد بن عبدالله العمراني');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عادل بن محمد بن عبدالعزيز السبيعي', '1000000059', '505901907',
       (SELECT id FROM buildings WHERE building_number = 'V59' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عادل بن محمد بن عبدالعزيز السبيعي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالمحسن بن محمد بن علي آل سميح', '1000000060', '505429217',
       (SELECT id FROM buildings WHERE building_number = 'V60' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالمحسن بن محمد بن علي آل سميح');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالعزيز بن سعد بن عمر العامر', '1000000061', '504109315',
       (SELECT id FROM buildings WHERE building_number = 'V61' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالعزيز بن سعد بن عمر العامر');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'سعد بن سعيد بن عائض القرني', '1000000062', '555111979',
       (SELECT id FROM buildings WHERE building_number = 'V62' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'سعد بن سعيد بن عائض القرني');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أسامة بن محمد إبراهيم الشيبان ', '1000000063', '547111179',
       (SELECT id FROM buildings WHERE building_number = 'V63' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أسامة بن محمد إبراهيم الشيبان ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'إيمان بنت محمد بن أحمد الرويثي', '1000000064', '504253422',
       (SELECT id FROM buildings WHERE building_number = 'V64' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'إيمان بنت محمد بن أحمد الرويثي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'طلال بن سعد بن سلمان البلوي', '1000000065', '581100344',
       (SELECT id FROM buildings WHERE building_number = 'V65' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'طلال بن سعد بن سلمان البلوي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أحمد بن صالح بن عبدالله السديس', '1000000066', '555453363',
       (SELECT id FROM buildings WHERE building_number = 'V66' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أحمد بن صالح بن عبدالله السديس');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'خالد بن ناصر بن صالح الشويرخ', '1000000067', '506624495',
       (SELECT id FROM buildings WHERE building_number = 'V67' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'خالد بن ناصر بن صالح الشويرخ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالله بن عبدالعزيز بن صالح الدغيثر', '1000000068', '504123662',
       (SELECT id FROM buildings WHERE building_number = 'V68' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالله بن عبدالعزيز بن صالح الدغيثر');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالله بن حضيض بن مزيد السلمي', '1000000069', '504239371',
       (SELECT id FROM buildings WHERE building_number = 'V69' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالله بن حضيض بن مزيد السلمي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'مازن بن عبدالرحمن بن رشيد بن مجلي', '1000000070', '506240299',
       (SELECT id FROM buildings WHERE building_number = 'V70' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'مازن بن عبدالرحمن بن رشيد بن مجلي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'محمد بن عائض ماجد التوم', '1000000071', '555566474',
       (SELECT id FROM buildings WHERE building_number = 'V71' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'محمد بن عائض ماجد التوم');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أحمد بن صالح بن محمد الصويان', '1000000072', '500353333',
       (SELECT id FROM buildings WHERE building_number = 'V72' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أحمد بن صالح بن محمد الصويان');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'وفاء بنت عبدالعزيز بن علي السويلم', '1000000073', '505236766',
       (SELECT id FROM buildings WHERE building_number = 'V73' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'وفاء بنت عبدالعزيز بن علي السويلم');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أحمد بن محمد بن عثمان المنيعي', '1000000074', '505425632',
       (SELECT id FROM buildings WHERE building_number = 'V74' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أحمد بن محمد بن عثمان المنيعي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'محمود بن سليمان بن صالح المحمود', '1000000075', '599966369',
       (SELECT id FROM buildings WHERE building_number = 'V75' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'محمود بن سليمان بن صالح المحمود');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'فهد بن سليمان بن إبراهيم الفهيد', '1000000076', '503440432',
       (SELECT id FROM buildings WHERE building_number = 'V76' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'فهد بن سليمان بن إبراهيم الفهيد');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالله بن يحيى بن جابر الفيفي', '1000000077', '555022910',
       (SELECT id FROM buildings WHERE building_number = 'V77' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالله بن يحيى بن جابر الفيفي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أسامة بن عبدالرحمن بن محمد الخميس', '1000000078', '500844476',
       (SELECT id FROM buildings WHERE building_number = 'V78' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أسامة بن عبدالرحمن بن محمد الخميس');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'إبراهيم بن محمد قاسم الميمن', '1000000079', '555138743',
       (SELECT id FROM buildings WHERE building_number = 'V79' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'إبراهيم بن محمد قاسم الميمن');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'حسن بن أحمد بن إبراهيم النعمي', '1000000080', '503409391',
       (SELECT id FROM buildings WHERE building_number = 'V80' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'حسن بن أحمد بن إبراهيم النعمي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'سالم بن علي بن صالح اليامي', '1000000081', '504939349',
       (SELECT id FROM buildings WHERE building_number = 'V81' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'سالم بن علي بن صالح اليامي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أحمد بن عبدالله بن محمد الضويحي', '1000000082', '505224887',
       (SELECT id FROM buildings WHERE building_number = 'V82' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أحمد بن عبدالله بن محمد الضويحي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أحمد بن محمد بن حمد الرزين', '1000000083', '553552911',
       (SELECT id FROM buildings WHERE building_number = 'V83' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أحمد بن محمد بن حمد الرزين');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'طارق بن عودة بن عبدالله العودة', '1000000084', '504226265',
       (SELECT id FROM buildings WHERE building_number = 'V84' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'طارق بن عودة بن عبدالله العودة');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'صالح بن ناصر بن صالح الشويرخ', '1000000085', '503234538',
       (SELECT id FROM buildings WHERE building_number = 'V85' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'صالح بن ناصر بن صالح الشويرخ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'تركي بن سعد بن فهيد الهويمل', '1000000086', '505473462',
       (SELECT id FROM buildings WHERE building_number = 'V86' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'تركي بن سعد بن فهيد الهويمل');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'محمد بن عبدالله بن عبدالعزيز الراشد', '1000000087', '564951910',
       (SELECT id FROM buildings WHERE building_number = 'V87' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'محمد بن عبدالله بن عبدالعزيز الراشد');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'أحمد بن سعد ناصر الأحمد', '1000000088', '502338811',
       (SELECT id FROM buildings WHERE building_number = 'V88' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'أحمد بن سعد ناصر الأحمد');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'محمد بن محسن بن سالم بابطين', '1000000089', '555232144',
       (SELECT id FROM buildings WHERE building_number = 'V89' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'محمد بن محسن بن سالم بابطين');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'حصة بنت إبراهيم بن علي الجريوي', '1000000090', '547776689',
       (SELECT id FROM buildings WHERE building_number = 'V90' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'حصة بنت إبراهيم بن علي الجريوي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'سعد بن علي بن عبدالله الوابل ', '1000000091', '554999454',
       (SELECT id FROM buildings WHERE building_number = 'V91' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'سعد بن علي بن عبدالله الوابل ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'ناصر بن صالح بن ناصر العود', '1000000092', '503338341',
       (SELECT id FROM buildings WHERE building_number = 'V92' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'ناصر بن صالح بن ناصر العود');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'عبدالله بن محمد بن ظافر القرني', '1000000093', '530014666',
       (SELECT id FROM buildings WHERE building_number = 'V93' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'عبدالله بن محمد بن ظافر القرني');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'موضي بنت صالح بن علي اللحيدان', '1000000094', '506471979',
       (SELECT id FROM buildings WHERE building_number = 'V94' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'موضي بنت صالح بن علي اللحيدان');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'بدر بن محمد بن ناصر البشر ', '1000000095', '555218883',
       (SELECT id FROM buildings WHERE building_number = 'V95' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'بدر بن محمد بن ناصر البشر ');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'سليمان بن محمد بن غانم السدلان', '1000000096', '505151548',
       (SELECT id FROM buildings WHERE building_number = 'V96' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'سليمان بن محمد بن غانم السدلان');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'نايف بن محمد عايض العتيبي', '1000000097', '504171026',
       (SELECT id FROM buildings WHERE building_number = 'V97' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'نايف بن محمد عايض العتيبي');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'هلالة بنت براك بن عايد الشمري', '1000000098', '503487994',
       (SELECT id FROM buildings WHERE building_number = 'V98' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'هلالة بنت براك بن عايد الشمري');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'محمد بن خالد بن محمد البداح', '1000000099', '503166887',
       (SELECT id FROM buildings WHERE building_number = 'V99' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'محمد بن خالد بن محمد البداح');

INSERT INTO residents (name, national_id, phone, building_id, unit_number, is_active)
SELECT 'خالد بن محمد بن عبدالعزيز اليوسف', '1000000100', '555230959',
       (SELECT id FROM buildings WHERE building_number = 'V100' LIMIT 1),
       '0', true
WHERE NOT EXISTS (SELECT 1 FROM residents WHERE name = 'خالد بن محمد بن عبدالعزيز اليوسف');

COMMIT;
