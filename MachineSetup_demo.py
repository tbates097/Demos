import os
import sys
import tkinter as tk
from tkinter import filedialog

sys.dont_write_bytecode = True

sys.path.append(r"K:\10. Released Software\Shared Python Programs\production-2.1")
# For updated GenerateMCD_v2, add the automated-checkout-bench directory
sys.path.insert(0, r"C:\Users\tbates\Python\automated-checkout-bench")
from GenerateMCD_v2 import AerotechController

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main_menu():
    """Prints the main menu options."""
    print("\n" + "="*70)
    print("      Aerotech MCD Generation Demo v2.0")
    print("      (Enhanced with Drive Configuration System)")
    print("="*70)
    print("1. WF1: Create CALCULATED MCD with drive-specific config")
    print("2. WF2: Create NON-CALCULATED MCD with drive-specific config")
    print("3. WF3: Convert existing MCD file to JSON")
    print("4. WF4: RECALCULATE & EXTRACT parameters from existing MCD")
    print("5. Show Available Drive Types & Info")
    print("6. Test Configuration Validation")
    print("0. Exit")
    print("-"*70)
    return input("Select an option (0-6): ")

def show_available_drives(mcd_processor):
    """Display available drive types with information"""
    print("\n🔍 --- Available Drive Types ---")
    print("="*50)
    
    try:
        drives_with_info = mcd_processor.get_available_drives_with_info()
        
        print(f"Found {len(drives_with_info)} configured drive types:\n")
        
        for drive in drives_with_info:
            status = "✅" if drive['template_exists'] else "❌"
            multi_axis = "Multi-Axis" if drive['is_multi_axis'] else "Single-Axis"
            
            print(f"{status} {drive['type']:8} - {drive['display_name']}")
            print(f"   Type: {multi_axis} {drive['controller_type']}")
            print(f"   Options: {drive['electrical_options_count']} total, {drive['required_options_count']} required")
            
            if drive['template_exists']:
                # Show default config
                default_config = mcd_processor.get_default_electrical_config(drive['type'])
                if default_config:
                    config_preview = ', '.join([f"{k}: {v}" for k, v in list(default_config.items())[:2]])
                    if len(default_config) > 2:
                        config_preview += f", ... (+{len(default_config) - 2} more)"
                    print(f"   Defaults: {config_preview}")
            else:
                print(f"   ⚠️  Template missing: {drive['template_file']}")
            print()
    
    except Exception as e:
        print(f"❌ Error: {e}")

def test_validation(mcd_processor):
    """Test the validation system with various configurations"""
    print("\n✅ --- Configuration Validation Test ---")
    print("="*50)
    
    test_cases = [
        {
            'name': 'Valid Configuration',
            'drive': 'iXA4',
            'specs': {'Travel': '-025', 'Feedback': '-E1'},
            'electrical': {'Bus Voltage': '160', 'Motor Supply Voltage': '-AC', 'Current Axes 1 and 2': '-20'}
        },
        {
            'name': 'Mixed Configuration (should fail)',
            'drive': 'iXA4', 
            'specs': {'Travel': '-025', 'Bus Voltage': '160'},  # Bus voltage in wrong dict
            'electrical': {'Motor Supply Voltage': '-AC'}
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"{i}. Testing: {test['name']}")
        print(f"   Drive: {test['drive']}")
        print(f"   Specs: {test['specs']}")
        print(f"   Electrical: {test['electrical']}")
        
        validation = mcd_processor.validate_configuration_setup(
            test['specs'], test['electrical'], test['drive']
        )
        
        if validation['valid']:
            print("   ✅ PASSED")
        else:
            print("   ❌ FAILED - Errors:")
            for error in validation['errors']:
                print(f"      • {error}")
        print()

def run_workflow_1(mcd_processor):
    """WF1: Create calculated MCD with drive-specific configuration"""
    print("\n🏭 --- Workflow 1: Advanced Calculated MCD Generation ---")
    
    # Show available drives and let user choose
    drives_with_info = mcd_processor.get_available_drives_with_info()
    available_drives = [d for d in drives_with_info if d['template_exists']][:3]  # First 3 with templates
    
    if not available_drives:
        print("❌ No drives with templates found!")
        return None
    
    print("Available drives:")
    for i, drive in enumerate(available_drives, 1):
        print(f"{i}. {drive['type']} - {drive['display_name']}")
    
    try:
        choice = int(input(f"Select drive (1-{len(available_drives)}): ")) - 1
        selected_drive = available_drives[choice]
        drive_type = selected_drive['type']
    except (ValueError, IndexError):
        print("❌ Invalid selection, using iXA4")
        drive_type = 'iXA4'
    
    print(f"\nUsing drive: {drive_type}")
    
    # Separated configurations
    specs_dict = {
        'Travel': '-025',
        'Feedback': '-E1', 
        'Cable Management': '-CMS2'
    }
    
    # Get default electrical config for selected drive
    electrical_dict = mcd_processor.get_default_electrical_config(drive_type)
    
    stage_type = 'DemoStage'
    axis = 'ST01'
    
    print(f"Mechanical specs: {specs_dict}")
    print(f"Electrical specs: {electrical_dict}")
    
    # Validate configuration
    validation = mcd_processor.validate_configuration_setup(specs_dict, electrical_dict, drive_type)
    if not validation['valid']:
        print(f"❌ Configuration validation failed: {validation['errors']}")
        return None
    print("✅ Configuration validation passed!")
    
    try:
        calculated_mcd, warnings, output_path = mcd_processor.calculate_parameters(
            specs_dict=specs_dict,
            electrical_dict=electrical_dict,
            stage_type=stage_type, 
            axis=axis,
            drive_type=drive_type
        )
        print(f"\n✅ Success! Calculated MCD saved to: {output_path}")
        if warnings:
            print(f"⚠️ Warnings: {warnings}")
        return output_path
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def run_workflow_2(mcd_processor):
    """WF2: Create non-calculated MCD"""
    print("\n📄 --- Workflow 2: Non-Calculated MCD Generation ---")
    
    # Use MS template for simplicity
    drive_type = 'MS'
    specs_dict = {'Travel': '-100', 'Feedback': '-E1'}
    electrical_dict = {'Bus Voltage': '80'}
    
    print(f"Using {drive_type} template")
    print(f"Mechanical specs: {specs_dict}")
    print(f"Electrical specs: {electrical_dict}")
    
    try:
        mcd_obj, warnings, output_path = mcd_processor.json_to_mcd(
            specs_dict=specs_dict,
            electrical_dict=electrical_dict,
            stage_type='DemoStage', 
            axis='X',
            drive_type=drive_type
        )
        print(f"\n✅ Success! Non-calculated MCD saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def run_workflow_3(mcd_processor):
    """WF3: Convert MCD to JSON"""
    print("\n📄 --- Workflow 3: MCD → JSON Conversion ---")
    
    mcd_path = input("Enter MCD file path (or press Enter to cancel): ").strip().strip('"\'')
    if not mcd_path:
        print("Cancelled.")
        return
    
    if not os.path.exists(mcd_path):
        print(f"❌ File not found: {mcd_path}")
        return

    output_json_path = os.path.join(BASE_DIR, f"{os.path.basename(mcd_path).split('.')[0]}_converted.json")
    
    try:
        mcd_processor.mcd_to_json(mcd_path, output_json_path)
        print(f"✅ Success! JSON saved to: {output_json_path}")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_workflow_4(mcd_processor):
    """WF4: Recalculate and extract parameters"""
    print("\n🔄 --- Workflow 4: Recalculate & Extract Parameters ---")
    
    mcd_path = input("Enter MCD file path (or press Enter to cancel): ").strip().strip('"\'')
    if not mcd_path:
        print("Cancelled.")
        return
    
    if not os.path.exists(mcd_path):
        print(f"❌ File not found: {mcd_path}")
        return

    try:
        servo_params, ff_params, calculated_mcd, output_path, warnings = mcd_processor.recalculate_and_extract(
            mcd_path, save_recalculated=True
        )
        
        print(f"✅ Success! Recalculated MCD saved to: {output_path}")
        print(f"Extracted {len(servo_params)} servo and {len(ff_params)} feedforward parameters")
        
        if warnings:
            print(f"⚠️ Warnings: {warnings}")
            
        # Show sample parameters
        if servo_params:
            print("\nSample servo parameters:")
            for param, value in list(servo_params.items())[:3]:
                print(f"  {param}: {value}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        print("🚀 Initializing GenerateMCD v2.0 with Drive Configuration System...")
        
        # Create controller with enhanced file saving
        mcd_processor = AerotechController.with_file_saving(
            output_dir=os.path.join(BASE_DIR, "MCD_Output"),
            separate_dirs=True,
            overwrite=True
        )
        
        # Initialize
        mcd_processor.initialize()
        
        print("✅ GenerateMCD v2.0 initialized successfully!")
        
        # Show system info
        available_drives = mcd_processor.get_available_drives()
        drives_with_templates = [d['type'] for d in mcd_processor.get_available_drives_with_info() if d['template_exists']]
        
        print(f"\n📊 System Status:")
        print(f"   • Drive configurations: {len(available_drives)}")
        print(f"   • Available templates: {len(drives_with_templates)}")
        print(f"   • Output directory: {os.path.join(BASE_DIR, 'MCD_Output')}")
        
        if drives_with_templates:
            print(f"   • Ready drives: {', '.join(drives_with_templates[:4])}")
            if len(drives_with_templates) > 4:
                print(f"     (+{len(drives_with_templates) - 4} more)")

    except Exception as e:
        print(f"❌ CRITICAL ERROR during initialization: {e}")
        print("Please ensure all required files are available.")
        sys.exit(1)

    # Main menu loop
    while True:
        choice = main_menu()
        try:
            if choice == '1':
                run_workflow_1(mcd_processor)
            elif choice == '2':
                run_workflow_2(mcd_processor)
            elif choice == '3':
                run_workflow_3(mcd_processor)
            elif choice == '4':
                run_workflow_4(mcd_processor)
            elif choice == '5':
                show_available_drives(mcd_processor)
            elif choice == '6':
                test_validation(mcd_processor)
            elif choice == '0':
                print("Exiting demo. Thanks for testing GenerateMCD v2.0!")
                break
            else:
                print("❌ Invalid option. Please try again.")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            if hasattr(e, 'InnerException') and e.InnerException:
                print(f"Inner .NET Exception: {e.InnerException}")
        
        input("\nPress Enter to return to the menu...")