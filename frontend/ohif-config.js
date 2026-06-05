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
