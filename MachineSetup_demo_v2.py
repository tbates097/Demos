import os
import sys
import tkinter as tk
from tkinter import filedialog
import importlib

sys.dont_write_bytecode = True

#sys.path.append(r"K:\10. Released Software\Shared Python Programs\production-2.1")
# For testing, add the automated-checkout-bench directory to access the updated GenerateMCD_v2
#sys.path.insert(0, r"C:\Users\tbates\Python\automated-checkout-bench")

# Clear cache to ensure we get the latest version
if 'GenerateMCD_v2' in sys.modules:
    importlib.reload(sys.modules['GenerateMCD_v2'])

from GenerateMCD_v2 import AerotechController

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main_menu():
    """Prints the comprehensive main menu options."""
    print("\n" + "="*80)
    print("      Aerotech MCD Generation Demo v2.0 - Complete Feature Test")
    print("      (Drive Configuration System + Separated Configs)")
    print("="*80)
    print("🔍 DISCOVERY & EXPLORATION:")
    print("1. Discover Available Drive Types (with detailed info)")
    print("2. Explore Drive Configuration Options (interactive)")
    print("3. Generate Default Electrical Configurations")
    print("4. Test Configuration Validation System")
    print()
    print("🏭 MCD GENERATION WORKFLOWS:")
    print("5. Create CALCULATED MCD (drive-specific with validation)")
    print("6. Create NON-CALCULATED MCD (drive-specific)")
    print("7. Convert MCD file to JSON")
    print("8. RECALCULATE & EXTRACT parameters from existing MCD")
    print()
    print("🧪 ADVANCED TESTING:")
    print("9. Multi-Drive Configuration Comparison")
    print("10. Interactive Configuration Builder (CLI)")
    print("11. GUI Configuration Builder (NEW!)")
    print("12. Validation Error Testing")
    print()
    print("0. Exit")
    print("-"*80)
    return input("Select an option (0-12): ")

def discover_drive_types(mcd_processor):
    """WF1: Discover and display all available drive types with details"""
    print("\n🔍 --- Drive Type Discovery ---")
    print("="*60)
    
    try:
        # Get detailed drive information
        drives_with_info = mcd_processor.get_available_drives_with_info()
        
        if not drives_with_info:
            print("❌ No drive configurations found!")
            return
        
        print(f"Found {len(drives_with_info)} configured drive types:\n")
        
        for i, drive in enumerate(drives_with_info, 1):
            status = "✅" if drive['template_exists'] else "❌"
            multi_axis = "Multi-Axis" if drive['is_multi_axis'] else "Single-Axis"
            
            print(f"{i:2}. {status} {drive['type']:8} - {drive['display_name']}")
            print(f"     Description: {drive['description']}")
            print(f"     Type: {multi_axis} {drive['controller_type']}")
            print(f"     Options: {drive['electrical_options_count']} total, {drive['required_options_count']} required")
            
            if not drive['template_exists']:
                print(f"     ⚠️  Template file missing: {drive['template_file']}")
            print()
        
        return drives_with_info
        
    except Exception as e:
        print(f"❌ Error discovering drive types: {e}")
        return []

def explore_drive_configuration(mcd_processor):
    """WF2: Interactive exploration of drive configuration options"""
    print("\n🔧 --- Drive Configuration Explorer ---")
    print("="*60)
    
    # First, let user select a drive
    drives_with_info = mcd_processor.get_available_drives_with_info()
    if not drives_with_info:
        print("❌ No drive configurations found!")
        return
    
    print("Available drive types:")
    for i, drive in enumerate(drives_with_info, 1):
        status = "✅" if drive['template_exists'] else "❌"
        print(f"{i:2}. {status} {drive['type']} - {drive['display_name']}")
    
    try:
        choice = int(input(f"\nSelect drive to explore (1-{len(drives_with_info)}): ")) - 1
        if choice < 0 or choice >= len(drives_with_info):
            print("❌ Invalid selection!")
            return
        
        selected_drive = drives_with_info[choice]
        drive_type = selected_drive['type']
        
        print(f"\n🔧 Exploring {selected_drive['display_name']} Configuration")
        print("-" * 60)
        
        # Get detailed menu data
        menu_data = mcd_processor.get_drive_menu_data(drive_type)
        if not menu_data:
            print("❌ No configuration data available!")
            return
        
        drive_info = menu_data['drive_info']
        print(f"Drive Info:")
        print(f"  • Type: {drive_info['controller_type']}")
        print(f"  • Multi-axis: {drive_info['is_multi_axis']}")
        print(f"  • Description: {drive_info['description']}")
        print()
        
        print("Electrical Configuration Options:")
        print("-" * 40)
        
        for i, option in enumerate(menu_data['options'], 1):
            required_status = "⚠️ REQUIRED" if option['required'] else "Optional"
            choices_info = f"{len(option['choices'])} choices" if option['choices'] else "Text input"
            
            print(f"{i:2}. {option['name']} ({required_status})")
            print(f"     Description: {option['description']}")
            print(f"     Type: {option['type']}, {choices_info}")
            print(f"     Default: {option['default'] or 'None'}")
            
            if option['choices']:
                choices_str = ', '.join(option['choices'][:5])  # Show first 5
                if len(option['choices']) > 5:
                    choices_str += f", ... (+{len(option['choices']) - 5} more)"
                print(f"     Choices: {choices_str}")
            print()
        
        return drive_type
        
    except (ValueError, IndexError):
        print("❌ Invalid selection!")
        return None

def generate_default_configs(mcd_processor):
    """WF3: Generate and display default electrical configurations"""
    print("\n⚙️ --- Default Electrical Configuration Generator ---")
    print("="*60)
    
    drives_with_info = mcd_processor.get_available_drives_with_info()[:5]  # Show first 5
    
    print("Default electrical configurations for available drives:\n")
    
    for drive in drives_with_info:
        drive_type = drive['type']
        print(f"🔧 {drive['display_name']} ({drive_type})")
        print("-" * 50)
        
        try:
            default_config = mcd_processor.get_default_electrical_config(drive_type)
            
            if default_config:
                for key, value in default_config.items():
                    print(f"  • {key:25}: {value}")
            else:
                print("  (No default configuration available)")
            
        except Exception as e:
            print(f"  ❌ Error generating defaults: {e}")
        
        print()

def test_validation_system(mcd_processor):
    """WF4: Test the configuration validation system"""
    print("\n✅ --- Configuration Validation System Test ---")
    print("="*60)
    
    # Test with different drive types and configurations
    test_cases = [
        {
            'name': 'Valid iXA4 Configuration',
            'drive_type': 'iXA4',
            'specs_dict': {'Travel': '-025', 'Feedback': '-E1'},
            'electrical_dict': {'Bus Voltage': '160', 'Motor Supply Voltage': '-AC', 'Current Axes 1 and 2': '-20'}
        },
        {
            'name': 'Invalid Bus Voltage',
            'drive_type': 'iXA4', 
            'specs_dict': {'Travel': '-025', 'Feedback': '-E1'},
            'electrical_dict': {'Bus Voltage': '999', 'Motor Supply Voltage': '-AC'}  # Invalid voltage
        },
        {
            'name': 'Missing Required Options',
            'drive_type': 'iXA4',
            'specs_dict': {'Travel': '-025', 'Feedback': '-E1'},
            'electrical_dict': {'Bus Voltage': '160'}  # Missing required options
        },
        {
            'name': 'Mixed Configuration (should fail)',
            'drive_type': 'iXA4',
            'specs_dict': {'Travel': '-025', 'Bus Voltage': '160'},  # Bus voltage in wrong dict
            'electrical_dict': {'Motor Supply Voltage': '-AC'}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. Testing: {test_case['name']}")
        print(f"   Drive: {test_case['drive_type']}")
        print(f"   Specs: {test_case['specs_dict']}")
        print(f"   Electrical: {test_case['electrical_dict']}")
        
        try:
            validation = mcd_processor.validate_configuration_setup(
                test_case['specs_dict'],
                test_case['electrical_dict'], 
                test_case['drive_type']
            )
            
            if validation['valid']:
                print("   ✅ PASSED - Configuration is valid")
            else:
                print("   ❌ FAILED - Configuration errors found:")
                for error in validation['errors']:
                    print(f"      • {error}")
                
                if validation.get('electrical_validation', {}).get('suggestions'):
                    print("   💡 Suggestions:")
                    for option, suggestion in validation['electrical_validation']['suggestions'].items():
                        print(f"      • {option}: {suggestion}")
        
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
        
        print()

def create_calculated_mcd_advanced(mcd_processor):
    """WF5: Create calculated MCD with drive-specific configuration"""
    print("\n🏭 --- Advanced Calculated MCD Generation ---")
    print("="*60)
    
    # Let user select drive type
    drives_with_info = mcd_processor.get_available_drives_with_info()
    available_drives = [d for d in drives_with_info if d['template_exists']]
    
    if not available_drives:
        print("❌ No drives with valid templates found!")
        return
    
    print("Available drives with templates:")
    for i, drive in enumerate(available_drives[:5], 1):  # Show first 5
        print(f"{i}. {drive['type']} - {drive['display_name']}")
    
    try:
        choice = int(input(f"Select drive (1-{min(len(available_drives), 5)}): ")) - 1
        if choice < 0 or choice >= len(available_drives):
            print("❌ Invalid selection!")
            return
        
        selected_drive = available_drives[choice]
        drive_type = selected_drive['type']
        
        print(f"\n🔧 Generating MCD for {selected_drive['display_name']}")
        
        # Get default electrical configuration
        default_electrical = mcd_processor.get_default_electrical_config(drive_type)
        
        # Define mechanical specs
        specs_dict = {
            'Travel': '-025',
            'Feedback': '-E1', 
            'Cable Management': '-CMS2'
        }
        
        stage_type = 'ANT95L'
        axis = 'ST01'
        
        print(f"Mechanical specs: {specs_dict}")
        print(f"Electrical specs: {default_electrical}")
        
        # Validate configuration
        validation = mcd_processor.validate_configuration_setup(specs_dict, default_electrical, drive_type)
        
        if not validation['valid']:
            print("❌ Configuration validation failed:")
            for error in validation['errors']:
                print(f"  • {error}")
            return
        
        print("✅ Configuration validated successfully!")
        
        # Generate MCD
        calculated_mcd, warnings, output_path = mcd_processor.calculate_parameters(
            specs_dict=specs_dict,
            electrical_dict=default_electrical,
            stage_type=stage_type,
            axis=axis,
            drive_type=drive_type
        )
        
        print(f"\n✅ Success! Calculated MCD saved to: {output_path}")
        if warnings:
            print(f"⚠️ Warnings: {warnings}")
        
        return output_path
        
    except (ValueError, IndexError):
        print("❌ Invalid selection!")
        return None
    except Exception as e:
        print(f"❌ Error generating MCD: {e}")
        return None

def multi_drive_comparison(mcd_processor):
    """WF9: Compare configurations across different drive types"""
    print("\n🔄 --- Multi-Drive Configuration Comparison ---")
    print("="*60)
    
    drives_to_compare = ['iXA4', 'XC4e', 'XR3', 'MS']
    
    print("Comparing electrical configurations across drive types:\n")
    
    for drive_type in drives_to_compare:
        print(f"🔧 {drive_type}")
        print("-" * 30)
        
        try:
            # Check if drive exists
            drive_info = mcd_processor.get_drive_info(drive_type)
            if not drive_info or not drive_info.get('template_exists'):
                print(f"  ❌ Template not found for {drive_type}")
                print()
                continue
            
            # Get default configuration  
            default_config = mcd_processor.get_default_electrical_config(drive_type)
            
            if default_config:
                for key, value in default_config.items():
                    print(f"  • {key:20}: {value}")
            else:
                print("  (No default options)")
            
            # Show drive characteristics
            print(f"  Multi-axis: {drive_info.get('is_multi_axis', 'Unknown')}")
            print(f"  Type: {drive_info.get('controller_type', 'Unknown')}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()

def interactive_config_builder(mcd_processor):
    """WF10: Interactive configuration builder"""
    print("\n🎨 --- Interactive Configuration Builder ---")
    print("="*60)
    
    # Let user select drive
    drives_with_info = mcd_processor.get_available_drives_with_info()
    available_drives = [d for d in drives_with_info if d['template_exists']][:3]  # First 3 for demo
    
    if not available_drives:
        print("❌ No drives with valid templates found!")
        return
    
    print("Select a drive to configure:")
    for i, drive in enumerate(available_drives, 1):
        print(f"{i}. {drive['type']} - {drive['display_name']}")
    
    try:
        choice = int(input(f"Choice (1-{len(available_drives)}): ")) - 1
        if choice < 0 or choice >= len(available_drives):
            print("❌ Invalid selection!")
            return
        
        selected_drive = available_drives[choice]
        drive_type = selected_drive['type']
        
        print(f"\n🎨 Building configuration for {selected_drive['display_name']}")
        
        # Use the interactive configuration builder
        electrical_config = mcd_processor.create_electrical_config_interactively(drive_type)
        
        if electrical_config:
            print(f"\n🎉 Configuration created successfully!")
            print("Final electrical configuration:")
            for key, value in electrical_config.items():
                print(f"  • {key}: {value}")
            
            # Test it with an MCD generation
            test_generation = input("\nTest this configuration by generating an MCD? (y/N): ").lower().strip()
            if test_generation == 'y':
                specs_dict = {'Travel': '-025', 'Feedback': '-E1'}
                stage_type = 'ANT95L'
                try:
                    calculated_mcd, warnings, output_path = mcd_processor.calculate_parameters(
                        specs_dict=specs_dict,
                        electrical_dict=electrical_config,
                        stage_type=stage_type,
                        axis='ST01',
                        drive_type=drive_type
                    )
                    print(f"✅ Test MCD generated: {output_path}")
                except Exception as e:
                    print(f"❌ MCD generation failed: {e}")
        else:
            print("❌ Configuration creation failed or was cancelled")
        
    except (ValueError, IndexError):
        print("❌ Invalid selection!")

def gui_config_builder(mcd_processor):
    """WF11: GUI Configuration Builder with dropdown windows"""
    print("\n🖥️ --- GUI Configuration Builder (NEW!) ---")
    print("="*60)
    print("Opening GUI configuration window...")
    print("📋 Features:")
    print("  • User-friendly window interface")
    print("  • Dropdown menus for all options") 
    print("  • Real-time validation")
    print("  • Default value application")
    print("  • Drive selection dialog")
    print("\n💡 Note: Window will open in a separate GUI...")
    print("\n⚠️ IMPORTANT: Look for a new window that may have opened!")
    print("   • Check your taskbar for a new window")
    print("   • Try Alt+Tab to find the window")
    print("   • Check other monitors if you have multiple displays")
    
    try:
        # Launch the drive configuration GUI directly
        print("\n✅ Opening drive configuration window...")
        print("   Trying with explicit drive type (iXA4) for reliability...")
        
        # Try with explicit drive type instead of None
        electrical_config = mcd_processor.create_electrical_config_gui(drive_type="iXA4")
        
        # If we get here, the window was either shown or there was an error
        print("   GUI method returned. If you didn't see a window, there might be an issue.")
        
        if electrical_config:
            print(f"\n🎉 GUI Configuration completed successfully!")
            print("Final electrical configuration:")
            for key, value in electrical_config.items():
                print(f"  • {key}: {value}")
            
            # Test it with an MCD generation
            test_generation = input("\nTest this configuration by generating an MCD? (y/N): ").lower().strip()
            if test_generation == 'y':
                specs_dict = {'Travel': '-025', 'Feedback': '-E1'}
                
                # Get the drive type from the configuration result
                # For now, we'll ask the user since the GUI doesn't return the drive type
                print("\nAvailable drive types for MCD generation:")
                drives_info = mcd_processor.get_available_drives_with_info()
                drives_with_templates = [d for d in drives_info if d['template_exists']][:5]
                
                for i, drive in enumerate(drives_with_templates, 1):
                    print(f"{i}. {drive['type']} - {drive['display_name']}")
                
                try:
                    drive_choice = int(input(f"Which drive type was configured? (1-{len(drives_with_templates)}): ")) - 1
                    if 0 <= drive_choice < len(drives_with_templates):
                        drive_type = drives_with_templates[drive_choice]['type']
                        
                        calculated_mcd, warnings, output_path = mcd_processor.calculate_parameters(
                            specs_dict=specs_dict,
                            electrical_dict=electrical_config,
                            stage_type='ANT95L',
                            axis='ST01',
                            drive_type=drive_type
                        )
                        print(f"✅ Test MCD generated: {output_path}")
                    else:
                        print("❌ Invalid drive selection!")
                except Exception as e:
                    print(f"❌ MCD generation failed: {e}")
        else:
            print("\n❌ GUI Configuration cancelled by user")
            
    except Exception as e:
        print(f"❌ GUI Configuration error: {e}")
        print("💡 Make sure tkinter is available and the GUI module is accessible")

def validation_error_testing(mcd_processor):
    """WF12: Comprehensive validation error testing"""
    print("\n🧪 --- Validation Error Testing Suite ---")
    print("="*60)
    
    # Test various error conditions
    error_tests = [
        {
            'name': 'Unknown Drive Type',
            'drive_type': 'NONEXISTENT_DRIVE',
            'specs_dict': {'Travel': '-025'},
            'electrical_dict': {'Bus Voltage': '80'}
        },
        {
            'name': 'Electrical Option in Specs Dict',
            'drive_type': 'iXA4',
            'specs_dict': {'Travel': '-025', 'Bus Voltage': '160'},  # Wrong dict
            'electrical_dict': {'Motor Supply Voltage': '-AC'}
        },
        {
            'name': 'Invalid Electrical Choice',
            'drive_type': 'iXA4',
            'specs_dict': {'Travel': '-025'},
            'electrical_dict': {'Bus Voltage': '999', 'Motor Supply Voltage': 'INVALID'}
        },
        {
            'name': 'Empty Configuration',
            'drive_type': 'iXA4',
            'specs_dict': {},
            'electrical_dict': {}
        }
    ]
    
    for i, test in enumerate(error_tests, 1):
        print(f"{i}. {test['name']}")
        print(f"   Drive: {test['drive_type']}")
        print(f"   Specs: {test['specs_dict']}")
        print(f"   Electrical: {test['electrical_dict']}")
        
        try:
            validation = mcd_processor.validate_configuration_setup(
                test['specs_dict'],
                test['electrical_dict'],
                test['drive_type']
            )
            
            if validation['valid']:
                print("   😱 UNEXPECTED: Configuration passed validation!")
            else:
                print("   ✅ EXPECTED: Validation correctly failed")
                print("   Errors found:")
                for error in validation['errors']:
                    print(f"     • {error}")
                
                # Show suggestions if available
                suggestions = validation.get('electrical_validation', {}).get('suggestions', {})
                if suggestions:
                    print("   💡 Suggestions provided:")
                    for option, suggestion in suggestions.items():
                        print(f"     • {option}: {suggestion}")
        
        except Exception as e:
            print(f"   ✅ EXPECTED: Exception caught: {e}")
        
        print()

# Existing workflow functions (simplified versions)
def run_workflow_mcd_to_json(mcd_processor):
    """Convert MCD to JSON"""
    print("\n📄 --- Convert MCD to JSON ---")
    
    mcd_path = input("Enter MCD file path: ").strip().strip('"\'')
    if not mcd_path or not os.path.exists(mcd_path):
        print("❌ Invalid file path!")
        return
    
    output_json_path = os.path.join(BASE_DIR, f"{os.path.basename(mcd_path).split('.')[0]}_converted.json")
    
    try:
        mcd_processor.mcd_to_json(mcd_path, output_json_path)
        print(f"✅ Success! MCD converted to JSON: {output_json_path}")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")

def run_workflow_recalculate_extract(mcd_processor):
    """Recalculate and extract parameters"""
    print("\n🔄 --- Recalculate & Extract Parameters ---")
    
    mcd_path = input("Enter MCD file path: ").strip().strip('"\'')
    if not mcd_path or not os.path.exists(mcd_path):
        print("❌ Invalid file path!")
        return
    
    try:
        servo_params, ff_params, calculated_mcd, output_path, warnings = mcd_processor.recalculate_and_extract(
            mcd_path, save_recalculated=True
        )
        
        print(f"✅ Success! Recalculated MCD: {output_path}")
        print(f"Extracted {len(servo_params)} servo and {len(ff_params)} feedforward parameters")
        
        if warnings:
            print(f"⚠️ Warnings: {warnings}")
            
    except Exception as e:
        print(f"❌ Recalculation failed: {e}")

if __name__ == "__main__":
    try:
        print("🚀 Initializing GenerateMCD v2.0...")
        
        # Create controller with file saving enabled
        mcd_processor = AerotechController.with_file_saving(
            output_dir=os.path.join(BASE_DIR, "Demo_Output"),
            separate_dirs=True,
            overwrite=True
        )
        
        # Initialize the processor
        mcd_processor.initialize()
        
        print("✅ GenerateMCD v2.0 initialized successfully!")
        
        # Show initialization summary
        available_drives = mcd_processor.get_available_drives()
        drives_with_templates = [d['type'] for d in mcd_processor.get_available_drives_with_info() if d['template_exists']]
        
        print(f"📊 System Summary:")
        print(f"   • Drive configurations loaded: {len(available_drives)}")
        print(f"   • Drives with templates: {len(drives_with_templates)}")
        print(f"   • Output directory: {os.path.join(BASE_DIR, 'Demo_Output')}")
        
        if drives_with_templates:
            print(f"   • Ready drives: {', '.join(drives_with_templates[:5])}")
            if len(drives_with_templates) > 5:
                print(f"     ... and {len(drives_with_templates) - 5} more")

    except Exception as e:
        print(f"❌ CRITICAL ERROR during initialization: {e}")
        print("Please ensure GenerateMCD_v2.py and drive_config.json are available.")
        sys.exit(1)

    # Main demo loop
    while True:
        choice = main_menu()
        
        try:
            if choice == '1':
                discover_drive_types(mcd_processor)
            elif choice == '2':
                explore_drive_configuration(mcd_processor)
            elif choice == '3':
                generate_default_configs(mcd_processor)
            elif choice == '4':
                test_validation_system(mcd_processor)
            elif choice == '5':
                create_calculated_mcd_advanced(mcd_processor)
            elif choice == '6':
                # Simplified non-calculated MCD (using defaults)
                print("Creating non-calculated MCD with MS template...")
                specs_dict = {'Travel': '-025', 'Feedback': '-E1'}
                electrical_dict = {'Bus Voltage': '80'}
                _, _, output_path = mcd_processor.json_to_mcd(
                    specs_dict=specs_dict, electrical_dict=electrical_dict,
                    stage_type='ANT95L', axis='ST01', drive_type='MS'
                )
                print(f"✅ Non-calculated MCD saved: {output_path}")
            elif choice == '7':
                run_workflow_mcd_to_json(mcd_processor)
            elif choice == '8':
                run_workflow_recalculate_extract(mcd_processor)
            elif choice == '9':
                multi_drive_comparison(mcd_processor)
            elif choice == '10':
                interactive_config_builder(mcd_processor)
            elif choice == '11':
                gui_config_builder(mcd_processor)
            elif choice == '12':
                validation_error_testing(mcd_processor)
            elif choice == '0':
                print("🎉 Thanks for testing GenerateMCD v2.0!")
                break
            else:
                print("❌ Invalid option. Please try again.")
                
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            import traceback
            print("Full error details:")
            traceback.print_exc()
        
        input("\nPress Enter to continue...")
