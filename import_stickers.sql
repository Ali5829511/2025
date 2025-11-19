-- استيراد بيانات الملصقات
BEGIN;


INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1049763921',
       (SELECT id FROM residents WHERE name LIKE '%ناصر%' LIMIT 1),
       'د هـ ك 8466', 'هونداي كحلي 2018 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ناصر%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1045321443',
       (SELECT id FROM residents WHERE name LIKE '%أحمد%' LIMIT 1),
       'ر ا ص 5407', 'فورد تورس-سيدان  أزرق كحلي 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%أحمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1020592604',
       (SELECT id FROM residents WHERE name LIKE '%محمد%' LIMIT 1),
       'هـ ح ب 614', 'Z350  فضي 2005 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%محمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1013580699',
       (SELECT id FROM residents WHERE name LIKE '%محمد%' LIMIT 1),
       'د أ ي ٧٢٩٥', 'هونداي رمادي 2017 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%محمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1065462531',
       (SELECT id FROM residents WHERE name LIKE '%عبدالله%' LIMIT 1),
       'ح ط ه 4819', 'هوندا أوديسي فضي 2014 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالله%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1071969842',
       (SELECT id FROM residents WHERE name LIKE '%محمد%' LIMIT 1),
       'د ص ي 1575', 'هيونداي أكسنت فضي 2019 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%محمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '2228699688',
       (SELECT id FROM residents WHERE name LIKE '%لطفى%' LIMIT 1),
       'ح م ب 6103', 'نيسان صني فضي 2014 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%لطفى%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1004170237',
       (SELECT id FROM residents WHERE name LIKE '%سليمان%' LIMIT 1),
       'ح د ط ٥١٠٠', 'لكزس رمادي 2014 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سليمان%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1017478296',
       (SELECT id FROM residents WHERE name LIKE '%محمد%' LIMIT 1),
       'ر ب د 2661', 'سوزوكي', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%محمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1027393600',
       (SELECT id FROM residents WHERE name LIKE '%طلال%' LIMIT 1),
       'هـ ن أ 178', 'انفنتي أبيض 2019 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%طلال%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1017478296',
       (SELECT id FROM residents WHERE name LIKE '%محمد%' LIMIT 1),
       'ر ب د ٢٦٦١', 'سوزوكي بني فاتح 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%محمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1019211562',
       (SELECT id FROM residents WHERE name LIKE '%سعيد%' LIMIT 1),
       'ح س د 6437', 'اكسبدشن اسود 2014 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سعيد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1008302307',
       (SELECT id FROM residents WHERE name LIKE '%عبير%' LIMIT 1),
       'د ي ق 2866', 'بيجو  أسود  2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبير%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1047855828',
       (SELECT id FROM residents WHERE name LIKE '%أحمد%' LIMIT 1),
       'ر ح ح 3804', 'فاو  أزرق 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%أحمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1036932612',
       (SELECT id FROM residents WHERE name LIKE '%ناصر%' LIMIT 1),
       'د ر ص 6490', 'هونداي رمادي 2017 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ناصر%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1029647656',
       (SELECT id FROM residents WHERE name LIKE '%سعيد%' LIMIT 1),
       'ح د ر ٤٦٦٦', 'جمس يوكن بني فاتح 2013 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سعيد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1029647656',
       (SELECT id FROM residents WHERE name LIKE '%سعيد%' LIMIT 1),
       'د م ق 9119', 'فورد أبيض', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سعيد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1029647656',
       (SELECT id FROM residents WHERE name LIKE '%سعيد%' LIMIT 1),
       'د ق ك 1188', 'هونداي أكسنت 2019', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سعيد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1014293342',
       (SELECT id FROM residents WHERE name LIKE '%يوسف%' LIMIT 1),
       'أ ع ر ٢٧٨٢', 'انوفا فضي 2008 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%يوسف%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1009873207',
       (SELECT id FROM residents WHERE name LIKE '%فلوه%' LIMIT 1),
       'ر أ و 6368 ', 'شانجان احمر غامق 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%فلوه%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1049019498',
       (SELECT id FROM residents WHERE name LIKE '%أريج%' LIMIT 1),
       'د ق س 5209  SGD', 'هونداي النترا فضي 2020 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%أريج%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1049019498',
       (SELECT id FROM residents WHERE name LIKE '%أريج%' LIMIT 1),
       'ح ا د 4207  DAJ', 'فورد جراند ماركيز فضي 2010 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%أريج%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1049019498',
       (SELECT id FROM residents WHERE name LIKE '%أريج%' LIMIT 1),
       'ب هـ أ   1007  AHB', 'جمس يوكون فضي 2012 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%أريج%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1019938636',
       (SELECT id FROM residents WHERE name LIKE '%صالح%' LIMIT 1),
       'أ ل ط 6667', 'جمس بكب غمارتين أسود 2012 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%صالح%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1009873207',
       (SELECT id FROM residents WHERE name LIKE '%فلوه%' LIMIT 1),
       'د ص ي 3462', 'هونداي رمادي 2019 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%فلوه%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1029344239',
       (SELECT id FROM residents WHERE name LIKE '%خالد%' LIMIT 1),
       'BRA 3530', 'فورد رمادي 2016 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%خالد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1034108124',
       (SELECT id FROM residents WHERE name LIKE '%عبدالمجيد%' LIMIT 1),
       ' د ن م 3337', 'كيا  أسود 2017 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالمجيد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1044305124',
       (SELECT id FROM residents WHERE name LIKE '%هند%' LIMIT 1),
       '7467 ر ب م ', 'مازدا x5 بيج غامق 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%هند%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1065340984',
       (SELECT id FROM residents WHERE name LIKE '%نوره%' LIMIT 1),
       'د ق ب ٣٣٠٧', 'كامري  فضي  2019 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%نوره%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1066500362',
       (SELECT id FROM residents WHERE name LIKE '%سعود%' LIMIT 1),
       'ر ح م 8087', 'توسان هونداي رمادي 2023 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سعود%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1036932612',
       (SELECT id FROM residents WHERE name LIKE '%ناصر%' LIMIT 1),
       'ر ح ع ٩٥٤٤', 'تويوتا افالون أبيض  2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ناصر%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1013329493',
       (SELECT id FROM residents WHERE name LIKE '%أنس%' LIMIT 1),
       'ر ب ل 8560', 'تويوتا راش بني 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%أنس%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1006330565',
       (SELECT id FROM residents WHERE name LIKE '%سليمان%' LIMIT 1),
       'د و و 1246', 'برادو أبيض 2021 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سليمان%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1033329903',
       (SELECT id FROM residents WHERE name LIKE '%ياسر%' LIMIT 1),
       'ح أ ن 4404', 'تويوتا أبيض 2013 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ياسر%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1016869149',
       (SELECT id FROM residents WHERE name LIKE '%رياض%' LIMIT 1),
       'راب 9286', 'فولكس واجن رمادي 2021 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%رياض%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1046832364',
       (SELECT id FROM residents WHERE name LIKE '%عبدالرحمن%' LIMIT 1),
       'ر ح ر 1743', 'شانجان cs35 رمادي 2023 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالرحمن%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1071605560',
       (SELECT id FROM residents WHERE name LIKE '%منار%' LIMIT 1),
       'د ي د 1374', 'فولكس واجن اسود 2021 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%منار%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1030314700',
       (SELECT id FROM residents WHERE name LIKE '%علي%' LIMIT 1),
       'ر ح ق ٢٣٨٣', 'نيسان/ باترول  رصاصي 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%علي%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1063827958',
       (SELECT id FROM residents WHERE name LIKE '%محمد%' LIMIT 1),
       'JVD 1846', 'شيفرولية رمادي 2021 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%محمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1022746513',
       (SELECT id FROM residents WHERE name LIKE '%احمد%' LIMIT 1),
       'د ح ل 550', ' انفنتي  اسود  2019 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%احمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1005845613',
       (SELECT id FROM residents WHERE name LIKE '%عبدالله%' LIMIT 1),
       'راس5118', 'ازيرا رصاصي 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالله%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1005845613',
       (SELECT id FROM residents WHERE name LIKE '%عبدالله%' LIMIT 1),
       'بطط1663', 'اكسبيدشن رصاصي 2011 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالله%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1026385037',
       (SELECT id FROM residents WHERE name LIKE '%عبدالله%' LIMIT 1),
       'د و ع ٢٧٨١', 'جيبMG اسود 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالله%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1053818744',
       (SELECT id FROM residents WHERE name LIKE '%ناصر%' LIMIT 1),
       'دول ٢٥٥٤', 'انفينتي ابيض 2021 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ناصر%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1066537521',
       (SELECT id FROM residents WHERE name LIKE '%افنان%' LIMIT 1),
       'د م ط 3848', 'هونداي رمادي 2020 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%افنان%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1057076778',
       (SELECT id FROM residents WHERE name LIKE '%عاصم%' LIMIT 1),
       'درو ٣٠٥٦', 'توسان بني 2018 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عاصم%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1046550503',
       (SELECT id FROM residents WHERE name LIKE '%سارة%' LIMIT 1),
       'ح ص ه 1356', 'فورد فليكس رمادي 2013 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سارة%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1046550503',
       (SELECT id FROM residents WHERE name LIKE '%سارة%' LIMIT 1),
       'د ب ك 9212', 'لكزس أبيض 2017 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سارة%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1026056646',
       (SELECT id FROM residents WHERE name LIKE '%ابراهيم%' LIMIT 1),
       'د ل ه ٨٢٢٠', 'هونداي فضي 2020 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ابراهيم%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1037663315',
       (SELECT id FROM residents WHERE name LIKE '%علي%' LIMIT 1),
       'د ل و 7855', 'يوكن أسود 2020 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%علي%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1037663315',
       (SELECT id FROM residents WHERE name LIKE '%علي%' LIMIT 1),
       'ح ل ن 8467', 'تورس سيدان أسود 2015 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%علي%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1067640365',
       (SELECT id FROM residents WHERE name LIKE '%منصور%' LIMIT 1),
       '٨٦١٤ ر ب م', 'مازدا رصاصي فضي 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%منصور%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1036005161',
       (SELECT id FROM residents WHERE name LIKE '%نسرين%' LIMIT 1),
       'د ع س ٥٢٨٢', 'فان هوندا ابيض 2019 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%نسرين%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1001030400',
       (SELECT id FROM residents WHERE name LIKE '%فهد%' LIMIT 1),
       'ع ب ك 806', 'جييب احمر 1994 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%فهد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1021831753',
       (SELECT id FROM residents WHERE name LIKE '%امل%' LIMIT 1),
       'أ س م 9050', 'بكب غمارة بيضاء 1997 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%امل%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1001030400',
       (SELECT id FROM residents WHERE name LIKE '%فهد%' LIMIT 1),
       'ب ب ن 4822', 'جمس احمر 2015 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%فهد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1036544573',
       (SELECT id FROM residents WHERE name LIKE '%خليل%' LIMIT 1),
       'ر ا ا ٤٧٧٢', 'مازدا رمادي 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%خليل%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1004865695',
       (SELECT id FROM residents WHERE name LIKE '%بدر%' LIMIT 1),
       'ح أ ص 7441', 'تويوتا إنوفا أبيض 2013 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%بدر%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1045967088',
       (SELECT id FROM residents WHERE name LIKE '%عبدالله%' LIMIT 1),
       'د ط ح 8057', 'سوناتا فضي 2018 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالله%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1024194704',
       (SELECT id FROM residents WHERE name LIKE '%غاليه%' LIMIT 1),
       'ر ح ن 6550', 'شانجان ايدو بلس فضي 2023 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%غاليه%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1030301095',
       (SELECT id FROM residents WHERE name LIKE '%فاطمه%' LIMIT 1),
       'د م ط 1490', 'فورتشنر أسود 2021 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%فاطمه%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1030301095',
       (SELECT id FROM residents WHERE name LIKE '%فاطمه%' LIMIT 1),
       'ب ي ص 5245', 'فيلكس أسود 2013 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%فاطمه%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1030301095',
       (SELECT id FROM residents WHERE name LIKE '%فاطمه%' LIMIT 1),
       'ددم 1207', 'اكسنت أبيض 2017 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%فاطمه%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1012539340',
       (SELECT id FROM residents WHERE name LIKE '%صالح%' LIMIT 1),
       'ب ه ق ٣٠٨٩', 'تاهو ذهبي 2012 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%صالح%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1011784152',
       (SELECT id FROM residents WHERE name LIKE '%احمد%' LIMIT 1),
       'أ د ن 7656', 'فورد  أسود 2008 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%احمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1022869422',
       (SELECT id FROM residents WHERE name LIKE '%ابراهيم%' LIMIT 1),
       'م ق ح ٨٨٨', 'جيب لاندكروزر أبيض 2015 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ابراهيم%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1026324457',
       (SELECT id FROM residents WHERE name LIKE '%أحمد%' LIMIT 1),
       'ر ب ل', 'toyta أبيض 7351 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%أحمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1076621992',
       (SELECT id FROM residents WHERE name LIKE '%يوسف%' LIMIT 1),
       'ر ا و 9230', 'سيدان رمادي 2021 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%يوسف%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1018052108',
       (SELECT id FROM residents WHERE name LIKE '%مزنه%' LIMIT 1),
       'د ب ل  ٧١٣٨', 'سيان - كيا رصاصي 2017 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%مزنه%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1051711149',
       (SELECT id FROM residents WHERE name LIKE '%رائد%' LIMIT 1),
       'ح س ع 6260', 'اكسبلورر أبيض 2014 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%رائد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1044305124',
       (SELECT id FROM residents WHERE name LIKE '%هند%' LIMIT 1),
       'حدي 9585', 'يوكن ذهبي 2014 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%هند%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1049119918',
       (SELECT id FROM residents WHERE name LIKE '%عبدالله%' LIMIT 1),
       'ح ا ل 30', 'BMW أسود 2015 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالله%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1012131478',
       (SELECT id FROM residents WHERE name LIKE '%عهود%' LIMIT 1),
       'د ر س 226', 'جي اكس ار أبيض 2013 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عهود%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1012131478',
       (SELECT id FROM residents WHERE name LIKE '%عهود%' LIMIT 1),
       'د ح س 6600', 'تاهو أسود 2018 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عهود%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1027773090',
       (SELECT id FROM residents WHERE name LIKE '%دخيل%' LIMIT 1),
       'أ ن س 8520', 'سييرا بني 2013 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%دخيل%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1001030400',
       (SELECT id FROM residents WHERE name LIKE '%فهد%' LIMIT 1),
       'د ط أ 1349', 'كرايزلر رصاصي غامق 2014 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%فهد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1018345676',
       (SELECT id FROM residents WHERE name LIKE '%ريما%' LIMIT 1),
       'د ك ط 9355', 'جمس يوكن فضي 2020 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ريما%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1018345676',
       (SELECT id FROM residents WHERE name LIKE '%ريما%' LIMIT 1),
       'ر ح ر 2409', 'مازدا بني غامق 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ريما%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1027169190',
       (SELECT id FROM residents WHERE name LIKE '%عادل%' LIMIT 1),
       'د ل أ 7302', 'رينو تاليسمان أبيض 2018 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عادل%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1013333867',
       (SELECT id FROM residents WHERE name LIKE '%ابراهيم%' LIMIT 1),
       'ر ب ر 5008', 'هواندي رصاصي 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ابراهيم%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1068840238',
       (SELECT id FROM residents WHERE name LIKE '%مها%' LIMIT 1),
       'د ع ص 7053', 'لكزس es300 رصاصي 2019 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%مها%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1068840238',
       (SELECT id FROM residents WHERE name LIKE '%مها%' LIMIT 1),
       'د ي م 9374', 'انفنتي  ازرق غامق 2021', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%مها%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1048339202',
       (SELECT id FROM residents WHERE name LIKE '%عبدالعزيز%' LIMIT 1),
       '2949', 'لكزس es250 كحلي 2019 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالعزيز%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1048339202',
       (SELECT id FROM residents WHERE name LIKE '%عبدالعزيز%' LIMIT 1),
       '4989', 'شروكي رصاصي 2020', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالعزيز%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1048339202',
       (SELECT id FROM residents WHERE name LIKE '%عبدالعزيز%' LIMIT 1),
       'ر أ ك 4174', 'انفينتي أبيض 2020 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالعزيز%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1049794231',
       (SELECT id FROM residents WHERE name LIKE '%ضيف%' LIMIT 1),
       'درب 3689', 'جيب لاندكروزر ابيض 2018 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ضيف%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1049794231',
       (SELECT id FROM residents WHERE name LIKE '%ضيف%' LIMIT 1),
       'ح ص ح 2702', 'كامري فضي 2014', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ضيف%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1031003583',
       (SELECT id FROM residents WHERE name LIKE '%ريم%' LIMIT 1),
       'ح ص ي 8708', 'مازدا ابيض 2015 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ريم%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1029481577',
       (SELECT id FROM residents WHERE name LIKE '%سعد%' LIMIT 1),
       'ح ي ق 6874', 'اكسبيدشن رصاصي 2016 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سعد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1029481577',
       (SELECT id FROM residents WHERE name LIKE '%سعد%' LIMIT 1),
       'ب ر ه 6628', 'كيا كرنفال أخضر 2009', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سعد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1029481577',
       (SELECT id FROM residents WHERE name LIKE '%سعد%' LIMIT 1),
       'أ و م 9198', 'اوبترا سيدان فضي 2009', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سعد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1056264201',
       (SELECT id FROM residents WHERE name LIKE '%ساره%' LIMIT 1),
       'رأب ٤٤٥٠', 'مرسيدس اسود 2020 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ساره%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1008688929',
       (SELECT id FROM residents WHERE name LIKE '%وائل%' LIMIT 1),
       'ح م ط 6963', 'تويوتا فورتشنر أبيض 2015 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%وائل%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1025083708',
       (SELECT id FROM residents WHERE name LIKE '%سلطان%' LIMIT 1),
       'ب م س 8355', 'جمس يوكن ذهبي 2012 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سلطان%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1031760034',
       (SELECT id FROM residents WHERE name LIKE '%سمر%' LIMIT 1),
       'د ى م 9660', 'mazda gray 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%سمر%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1010536389',
       (SELECT id FROM residents WHERE name LIKE '%احمد%' LIMIT 1),
       'ر ب س 8716', 'فورد تورس أبيض 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%احمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1010536389',
       (SELECT id FROM residents WHERE name LIKE '%احمد%' LIMIT 1),
       'ر أ ع 5745', 'ميتسوبيشي اكسباندر فضي 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%احمد%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1049119918',
       (SELECT id FROM residents WHERE name LIKE '%عبدالله%' LIMIT 1),
       'د هـ ر 3601', 'جمس يوكن رمادي 2021 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالله%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1070334832',
       (SELECT id FROM residents WHERE name LIKE '%عبدالله%' LIMIT 1),
       'ح ر ب7725 ', 'جيب لكزس فضي 2017 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%عبدالله%');

INSERT INTO stickers (sticker_number, resident_id, plate_number, vehicle_type, issue_date, status)
SELECT '1024883652',
       (SELECT id FROM residents WHERE name LIKE '%ابراهيم%' LIMIT 1),
       'ر أ و 7348', 'هونداي, النترا  رصاصي 2022 ', CURRENT_DATE, 'active'
WHERE EXISTS (SELECT 1 FROM residents WHERE name LIKE '%ابراهيم%');

COMMIT;
