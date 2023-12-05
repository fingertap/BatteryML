# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.
from __future__ import annotations

import pickle

from enum import Enum
from typing import List


class StageMode(Enum):
    CHARGE = 1
    DISCHARGE = 2
    REST = 3


class StageData:
    def __init__(self,
                 voltage_in_V: List[float] = None,
                 current_in_A: List[float] = None,
                 time_in_s: List[float] = None,
                 temperature_in_C: List[float] = None,
                 **kwargs):
        # Determine the mode
        if max(current_in_A) > 1e-6:
            self.mode = StageMode.CHARGE
        elif min(current_in_A) < -1e-6:
            self.mode = StageMode.DISCHARGE
        else:
            self.mode = StageMode.REST

        self.voltage_in_V = voltage_in_V
        self.current_in_A = current_in_A
        self.time_in_s = time_in_s
        self.temperature_in_C = temperature_in_C

        self.additional_data = {}
        for key, val in kwargs.items():
            self.additional_data[key] = val

    def to_dict(self):
        return {
            'current_in_A': self.current_in_A,
            'voltage_in_V': self.voltage_in_V,
            'time_in_s': self.time_in_s,
            'temperature_in_C': self.temperature_in_C,
            **self.additional_data
        }


class CycleData:
    def __init__(self, stages: List[StageData | dict], **kwargs):
        self.stages = [
            stage if isinstance(stage, StageData) else StageData(**stage)
            for stage in stages
        ]
        self.additional_data = {}
        for key, val in kwargs.items():
            self.additional_data[key] = val

    def to_dict(self):
        return {
            'stages': [stage.to_dict() for stage in self.stages],
            **self.additional_data
        }


class BatteryData:
    def __init__(self,
                 cell_id: str,
                 *,
                 cycle_data: List[CycleData] = None,
                 form_factor: str = None,
                 anode_material: str = None,
                 cathode_material: str = None,
                 electrolyte_material: str = None,
                 nominal_capacity_in_Ah: float = None,
                 depth_of_charge: float = None,
                 depth_of_discharge: float = None,
                 already_spent_cycles: int = None,
                 max_voltage_limit_in_V: float = None,
                 min_voltage_limit_in_V: float = None,
                 max_current_limit_in_A: float = None,
                 min_current_limit_in_A: float = None,
                 reference: str = None,
                 description: str = None,
                 **kwargs):
        self.cell_id = cell_id
        self.cycle_data = cycle_data
        self.form_factor = form_factor
        self.anode_material = anode_material
        self.cathode_material = cathode_material
        self.electrolyte_material = electrolyte_material
        self.nominal_capacity_in_Ah = nominal_capacity_in_Ah
        self.depth_of_charge = depth_of_charge
        self.depth_of_discharge = depth_of_discharge
        self.already_spent_cycles = already_spent_cycles
        self.max_voltage_limit_in_V = max_voltage_limit_in_V
        self.min_voltage_limit_in_V = min_voltage_limit_in_V
        self.max_current_limit_in_A = max_current_limit_in_A
        self.min_current_limit_in_A = min_current_limit_in_A
        self.reference = reference
        self.description = description

        for key, val in kwargs.items():
            setattr(self, key, val)

    def to_dict(self):
        result = {}
        for key, val in self.__dict__.items():
            if not callable(val) and not key.startswith('_'):
                if hasattr(val, 'to_dict'):
                    result[key] = val.to_dict()
                else:
                    result[key] = val
        return result

    def dump(self, path: str):
        with open(path, 'wb') as fout:
            pickle.dump(self.to_dict(), fout)

    def __repr__(self):
        return f'<BatteryData: {self.cell_id}>'

    def __str__(self):
        details = []
        for key, val in self.__dict__.items():
            if key == 'cycle_data':
                details.append(f'cycles: {len(val)}')
            elif val:
                details.append(f'{key}: {val}')
        return '\n'.join(details)

    @staticmethod
    def load(path: str):
        with open(path, 'rb') as fin:
            obj = pickle.load(fin)
        return BatteryData(**obj)
