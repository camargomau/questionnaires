CREATE TABLE Respuestas (
    NumeroCuenta INT PRIMARY KEY,
    CaminoID INT,
    FinanzasID INT,
    HabilidadesID INT,
    HorarioID INT,
    PerfilID INT,
    RendimientoID INT,
    TecnologíaID INT
);

CREATE TABLE Dimension_Camino (
    CaminoID INT PRIMARY KEY AUTO_INCREMENT,
    NumeroCuenta INT,
    MayorPreocupacion VARCHAR(255),
    FactoresInfluyen VARCHAR(255),
    SituacionActual VARCHAR(255),
    TipoApoyo VARCHAR(255),
    HabilidadesEsenciales VARCHAR(255),
    PracticasInfluyen VARCHAR(255),
    VisualizacionCarrera VARCHAR(255),
    ValorEmpleo VARCHAR(255),
    UtilidadMaterialEstudio VARCHAR(255),
    RedContactosProfesionales BOOLEAN,
    AspectosMejorar VARCHAR(255),
    ContenidoActualizado VARCHAR(255)
);

CREATE TABLE Dimension_Finanzas (
    FinanzasID INT PRIMARY KEY AUTO_INCREMENT,
    NumeroCuenta INT,
    DineroGenerado DECIMAL(10, 2),
    GastosMensuales DECIMAL(10, 2),
    AhorroMensual DECIMAL(10, 2),
    DineroEmergencias DECIMAL(10, 2),
    Liquidez VARCHAR(255),
    InversionesCortoPlazo BOOLEAN,
    InversionesLargoPlazo BOOLEAN,
    PlanRetiro BOOLEAN,
    TarjetasCredito INT,
    PorcentajeCreditoDisponible DECIMAL(5, 2)
);

CREATE TABLE Dimension_Habilidades (
    HabilidadesID INT PRIMARY KEY AUTO_INCREMENT,
    NumeroCuenta INT,
    CapacidadExplicar VARCHAR(255),
    ComodidadEquipo VARCHAR(255),
    MayorDesafioEquipo VARCHAR(255),
    PreparacionTrabajoEquipo BOOLEAN,
    FacilidadConexiones VARCHAR(255),
    HablarAudiencia VARCHAR(255),
    TecnicasManejoEstres VARCHAR(255),
    PreparacionPresentaciones VARCHAR(255),
    HabilidadesTecnicasSuficientes BOOLEAN,
    AplicacionHabilidadesBlandas BOOLEAN,
    HabilidadesBlandasImportantes VARCHAR(255),
    HabilidadesFaltantes VARCHAR(255),
    PreparacionHabilidadesBlandas VARCHAR(255),
    SubestimacionHabilidadesBlandas BOOLEAN
);

CREATE TABLE Dimension_Horario (
    HorarioID INT PRIMARY KEY AUTO_INCREMENT,
    NumeroCuenta INT,
    ImpactoDesempenoAcademico VARCHAR(255),
    ImpactoDesempenoPersonal VARCHAR(255),
    DificultadesConcentracion VARCHAR(255),
    ImpactoOrganizacionTiempo VARCHAR(255),
    ImpactoRendimientoMateria BOOLEAN,
    ImpactoAlimentacionDescanso VARCHAR(255),
    SugerenciasMejora VARCHAR(255),
    ConsideracionDejarMateria BOOLEAN,
    HerramientasClase VARCHAR(255),
    MedioTransporte VARCHAR(255),
    DificultadesTransporte BOOLEAN,
    TiempoLlegadaCasa INT,
    SeguridadTransporte BOOLEAN,
    ModificacionRutas BOOLEAN
);

CREATE TABLE Dimension_Perfil (
    PerfilID INT PRIMARY KEY AUTO_INCREMENT,
    NumeroCuenta INT,
    Edad INT,
    Genero VARCHAR(50),
    EstadoResidencia VARCHAR(255),
    SituacionLaboral VARCHAR(255),
    TiempoRecorridoFacultad INT,
    InteresMaterias VARCHAR(255),
    Automovil BOOLEAN,
    AreaEspecialidadInteres VARCHAR(255),
    MateriaDificultad VARCHAR(255),
    MateriasAportadas VARCHAR(255),
    MateriasBarquear VARCHAR(255),
    TrabajoEquipo BOOLEAN,
    Perfeccionismo BOOLEAN,
    FamiliaRelacionada BOOLEAN,
    PreferenciaProyectos VARCHAR(255),
    ModeloSeguir VARCHAR(255),
    EquipoComputoAdecuado BOOLEAN,
    SoftwareComplejo VARCHAR(255),
    SoftwareFacil VARCHAR(255)
);

CREATE TABLE Dimension_Rendimiento (
    RendimientoID INT PRIMARY KEY AUTO_INCREMENT,
    NumeroCuenta INT,
    PromedioActual DECIMAL(3, 2),
    HorasEstudioSemanal DECIMAL(5, 2),
    MateriasActuales INT,
    MateriasReprobadas INT,
    AnosCarrera DECIMAL(3, 1),
    RaizMaterias VARCHAR(255),
    ApoyoProfesores BOOLEAN,
    FactoresExternos VARCHAR(255),
    SugerenciasMejoras VARCHAR(255),
    ExamenesJustos BOOLEAN,
    GestionTiempo VARCHAR(255)
);

CREATE TABLE Dimension_Tecnología (
    TecnologíaID INT PRIMARY KEY AUTO_INCREMENT,
    NumeroCuenta INT,
    Edad INT,
    Semestre INT,
    DispositivosFrecuentes VARCHAR(255),
    HorasUsoDiario DECIMAL(5, 2),
    UsoEscolar VARCHAR(255),
    RedesSociales VARCHAR(255),
    MotivoRedesSociales VARCHAR(255),
    MomentosAccesoRedes VARCHAR(255),
    UsoRedesTareas VARCHAR(255),
    ImpactoConcentracion VARCHAR(255),
    ImpactoRendimientoAcademico VARCHAR(255),
    CambiosConcentracion VARCHAR(255),
    ImpactoInteraccionEscolar VARCHAR(255),
    ConocimientoNormasTecnologia VARCHAR(255),
    FormacionPrivacidad VARCHAR(255),
    ExperienciaCiberacoso VARCHAR(255),
    PreparacionUsoResponsable VARCHAR(255),
    TalleresFormacionDeseados VARCHAR(255),
    InfluenciaEstadoAnimo VARCHAR(255),
    ImpactoComunicacionCompaneros VARCHAR(255),
    ImpactoAislamientoSocial VARCHAR(255),
    EstrategiasUsoSaludable VARCHAR(255),
    ActividadesEducacionDigital VARCHAR(255)
);
