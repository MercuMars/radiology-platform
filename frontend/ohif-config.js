// =========================================================
// 1. 跨 iframe 通信桥梁 (运行在 OHIF 内部)
// =========================================================
window.addEventListener('message', function(event) {
    if (event.data.action === 'GET_MEASUREMENTS') {
        console.log("[OHIF 内部] 收到外部父窗口获取测量数据的指令");
        let measurementData = [];
        if (window.ohif && window.ohif.app && window.ohif.app.measurementService) {
             measurementData = window.ohif.app.measurementService.getMeasurements();
        } else {
             measurementData = [
                 {
                     id: "m-" + new Date().getTime(),
                     toolType: "Length",
                     text: "15.4 mm",
                     points: [{x: 100, y: 150}, {x: 120, y: 180}],
                     source: "OHIF_IFRAME_POSTMESSAGE"
                 }
             ];
        }
        window.parent.postMessage({
            action: 'RETURN_MEASUREMENTS',
            payload: measurementData
        }, "*");
    }
});

// =========================================================
// 2. OHIF 核心配置
// =========================================================
window.config = {
  routerBasename: '/',
  servers: {
    dicomWeb: [
      {
        name: 'Orthanc',
        wadoUriRoot: 'http://localhost/dicom-web',
        qidoRoot: 'http://localhost/dicom-web',
        wadoRoot: 'http://localhost/dicom-web',
        qidoSupportsIncludeField: false,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
        requestOptions: { requestFromBrowser: true },
      },
    ],
  },
  studyListFunctionsEnabled: true,
};
