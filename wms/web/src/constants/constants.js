const WarehouseWeightUnits = [{
        value: 0,
        text: '克'
    },
    {
        value: 1,
        text: '千克'
    }
];

const CabinetOrientation = [{
        value: 0,
        text: '横向'
    },
    {
        value: 1,
        text: '竖向'
    }
];

const CabinetSize = [3,4,5,6,7,8,9,10,11,12]

const SortJobType = {
    CheckInboundParcelReadyToShip: 0,
    AllocateCabinetLattice: 1,
    CheckInboundParcelReadyToShipAndAllocateCabinetLattice: 2
}

export {
    WarehouseWeightUnits,
    CabinetOrientation,
    CabinetSize,
    SortJobType
}