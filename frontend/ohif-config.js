// =========================================================
// 1. 跨 iframe 通信桥梁 (运行在 OHIF 内部)
// =========================================================
window.addEventListener('message', function(event) {
    if (event.data.action === 'GET_MEASUREMENTS') {
        console.log("[OHIF 内部] 收到外部父窗口获取测量数据的指令");

        // 【说明】在官方编译好的 Docker 镜像中，内部的 React State 被高度封装。
        // 在未来的生产环境深度开发中，你需要编写一个 OHIF Extension 来向 window 对象暴露 measurementService。
        // 但作为 MVP，我们在这里验证通信链路已经完全打通。

        let measurementData = [];

        // 尝试探测是否存在暴露的全局变量
        if (window.ohif && window.ohif.app && window.ohif.app.measurementService) {
             measurementData = window.ohif.app.measurementService.getMeasurements();
        } else {
             // MVP 演示：证明数据能成功穿透 iframe 并进入外层数据库
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

        // 将抓取到的数据拨号"打回"给外层的父窗口
        window.parent.postMessage({
            action: 'RETURN_MEASUREMENTS',
            payload: measurementData
        }, "*");
    }
});

// =========================================================
// 2. 原有的 OHIF 核心配置
// =========================================================
window.config = {
  routerBasename: '/viewer',
  servers: {
    dicomWeb: [
      {
        name: 'Orthanc',
        wadoUriRoot: '/dicom-web',
        qidoRoot: '/dicom-web',
        wadoRoot: '/dicom-web',
        qidoSupportsIncludeField: false,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
        requestOptions: { requestFromBrowser: true },
      },
    ],
  },
  studyListFunctionsEnabled: true,
};
