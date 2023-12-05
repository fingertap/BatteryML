from batteryml.data.battery_data import (
    StageData, CycleData, BatteryData, StageMode
)

def test_stage_data_initialization():
    stage_data = StageData(
        voltage_in_V=[4.2, 4.1],
        current_in_A=[-0.3, -0.5],
        time_in_s=[10, 20],
        temperature_in_C=[25, 30],
        resistance_in_ohm=[0.3, 0.4])
    assert stage_data.voltage_in_V == [4.2, 4.1]
    assert stage_data.current_in_A == [-0.3, -0.5]
    assert stage_data.time_in_s == [10, 20]
    assert stage_data.temperature_in_C == [25, 30]
    assert stage_data.additional_data == {
        'resistance_in_ohm': [0.3, 0.4]
    }
    assert stage_data.mode == StageMode.DISCHARGE

def test_stage_data_to_dict():
    stage_data = StageData(
        voltage_in_V=[4.2, 4.1],
        current_in_A=[-0.3, -0.5],
        time_in_s=[10, 20],
        temperature_in_C=[25, 30],
        resistance_in_ohm=[0.3, 0.4])
    assert stage_data.to_dict() == {
        'voltage_in_V': [4.2, 4.1],
        'current_in_A': [-0.3, -0.5],
        'time_in_s': [10, 20],
        'temperature_in_C': [25, 30],
        'resistance_in_ohm': [0.3, 0.4]
    }
    

def test_cycle_data_initialization_with_dict():
    stage = {
        'voltage_in_V': [4.2],
        'current_in_A': [0.1],
        'time_in_s': [10],
        'temperature_in_C': [25]
    }
    cycle_data = CycleData(stages=[stage])
    assert len(cycle_data.stages) == 1
    assert cycle_data.stages[0].to_dict() == stage


def test_battery_data_initialization():
    battery_data = BatteryData(
        cell_id="cell123",
        form_factor="cylindrical",
        nominal_capacity_in_Ah=2.0)
    assert battery_data.cell_id == "cell123"
    assert battery_data.form_factor == "cylindrical"
    assert battery_data.nominal_capacity_in_Ah == 2.0


def test_battery_data_serialization(tmp_path):
    file_path = tmp_path / "battery_data.pkl"
    original_battery_data = BatteryData(
        cell_id="cell123", nominal_capacity_in_Ah=2.0)
    original_battery_data.dump(file_path)

    loaded_battery_data = BatteryData.load(file_path)
    assert loaded_battery_data.cell_id == "cell123"
    assert loaded_battery_data.nominal_capacity_in_Ah == 2.0
