import pytest

from extractor.converter.NdfToJsonConverter import NdfToJsonConverter

@pytest.fixture
def converter():
    return NdfToJsonConverter()

class TestNdfToJsonConverter:

    def test_convert_empty_string(self, converter):
        with pytest.raises(Exception):
            converter.convert_ndf_text('')

    def test_convert_whitespace_only_string(self, converter):
        result = converter.convert_ndf_text('    \n     \n     ')
        assert len(result) == 0

    def test_basic_item_type_name_field(self, converter):
        text = '\n  export Descriptor_Unit_Truck_WC52_US   \n    (  ) '
        result = converter.convert_ndf_text(text)
        assert result[0]['_type_name'] == 'Descriptor_Unit_Truck_WC52_US'

    def test_basic_item_base_name_field(self, converter):
        text = '\n  export Descriptor_Unit_Truck_WC52_US  is   TEntityDescriptor   \n    ( )\n'
        result = converter.convert_ndf_text(text)
        assert result[0]['_base_type_name'] == 'TEntityDescriptor'

    def test_multiple_basic_item_base_name_field(self, converter):
        text = '\n export Foo is Bar \n ( )\n export Foo2 is Bar2 \n ( ) \n'
        result = converter.convert_ndf_text(text)
        assert result[0]['_type_name'] == 'Foo'
        assert result[0]['_base_type_name'] == 'Bar'
        assert result[1]['_type_name'] == 'Foo2'
        assert result[1]['_base_type_name'] == 'Bar2'
        assert len(result) == 2

    def test_item_with_guid_field(self, converter):
        text = '\n  export Descriptor_Unit_Truck_WC52_US is TEntityDescriptor \n ( DescriptorId      = GUID:{85c06d35-a1ee-49ae-9b80-7356bdbdc5fd} ) '
        result = converter.convert_ndf_text(text)
        assert result[0]['DescriptorId'] == 'GUID:{85c06d35-a1ee-49ae-9b80-7356bdbdc5fd}'
    
    def test_item_with_string_field(self, converter):
        text = '\n  export Descriptor_Unit_Truck_WC52_US is TEntityDescriptor \n ( ClassNameForDebug = \'Unit_Truck_WC52_US\' ) '
        result = converter.convert_ndf_text(text)
        assert result[0]['ClassNameForDebug'] == 'Unit_Truck_WC52_US'

    def test_item_with_multiple_string_fields(self, converter):
        text = '\n  export Descriptor_Unit_Truck_WC52_US is TEntityDescriptor \n ( Foo = Bar Foo2 = \'Baz\' ClassNameForDebug = \'Unit_Truck_WC52_US\' ) '
        result = converter.convert_ndf_text(text)
        assert result[0]['Foo'] == 'Bar'
        assert result[0]['Foo2'] == 'Baz'
        assert result[0]['ClassNameForDebug'] == 'Unit_Truck_WC52_US'
    
    def test_item_with_empty_array_field(self, converter):
        text = '\n  export Descriptor_Unit_Truck_WC52_US is TEntityDescriptor \n ( Modules = [ ] ) '
        result = converter.convert_ndf_text(text)
        assert len(result[0]['Modules']) == 0

    def test_item_with_multiple_empty_array_field(self, converter):
        text = '\n  export Descriptor_Unit_Truck_WC52_US is TEntityDescriptor \n ( Modules = [ ] Foo = [ ] ) '
        result = converter.convert_ndf_text(text)
        assert len(result[0]['Modules']) == 0
        assert len(result[0]['Foo']) == 0
    
    def test_item_with_multiple_empty_array_and_text_field(self, converter):
        text = '\n  export Descriptor_Unit_Truck_WC52_US is TEntityDescriptor \n ( Modules = [ ] Foo = [ ] Bar = Baz ) '
        result = converter.convert_ndf_text(text)
        assert len(result[0]['Modules']) == 0
        assert len(result[0]['Foo']) == 0
        assert result[0]['Bar'] == 'Baz'

    def test_object_type_in_simple_array(self, converter):
        text = '\n  export Descriptor_Unit_Truck_WC52_US is TEntityDescriptor \n ( Modules = [ TModuleSelector \n (  \n Default  = TTypeUnitModuleDescriptor \n ( AcknowUnitType = ~/TAcknowUnitType_Transport ) ), ] ) '
        result = converter.convert_ndf_text(text)
        assert result[0]['Modules'][0]['_type_name'] == 'TModuleSelector'
        assert result[0]['Modules'][0]['Default']['AcknowUnitType'] == '~/TAcknowUnitType_Transport'
        assert result[0]['Modules'][0]['Default']['_base_type_name'] == 'TTypeUnitModuleDescriptor'
        
    def test_array_string_list(self, converter):
        text = '\n export Bar2 is Bar3 ( DescriptorId = GUID:{a-b-c-d-e} ClassNameForDebug = \'Foo2\' Modules = [ TFlagsModuleDescriptor ( InitialFlagSet = [ Flag_Foo, Flag_Bar, Flag_Baz, ] ), ] )'        
        result = converter.convert_ndf_text(text)
        assert result[0]['Modules'][0]['_type_name'] == 'TFlagsModuleDescriptor'
        assert len(result[0]['Modules'][0]['InitialFlagSet']) == 3
        assert result[0]['Modules'][0]['InitialFlagSet'][0] == 'Flag_Foo'
        assert result[0]['Modules'][0]['InitialFlagSet'][1] == 'Flag_Bar'
        assert result[0]['Modules'][0]['InitialFlagSet'][2] == 'Flag_Baz'

    def test_ignore_comments(self, converter):
        text = '\n  export //Sit // Lorem ipsum dolor \n Foo is // = ( [ \n Bar \n ( // Ipsum = \n Lorem // dolor === \n = \'Baz\' ) '
        result = converter.convert_ndf_text(text)
        assert result[0]['Lorem'] == 'Baz'
    
    def test_mixed_array_items(self, converter):
        text = '\n  export Descriptor_Unit_Truck_WC52_US is TEntityDescriptor \n ( Modules = [ ~/Dolor, Foo ( Default = Bar ( Baz = Lorem1 Baz2 = Lorem2 ) Selection = [ Foo2, Foo3 ( Condition  = MyBaseType2 ( ParamId=~/Foo4 ParamValue=~/Foo5 ) Descriptor = MyBaseType3 ( Baz3 = \'Lorem3\' Baz4 = Lorem4 ) ) ] ), ] ) '
        result = converter.convert_ndf_text(text) 
        assert len(result[0]['Modules']) == 2
        assert result[0]['Modules'][0] == '~/Dolor'

    def test_selector_module_example(self, converter):
        text = '\n  export Descriptor_Unit_Truck_WC52_US is TEntityDescriptor \n ( Modules = [ Foo ( Default = Bar ( Baz = Lorem1 Baz2 = Lorem2 ) Selection = [ Foo2, Foo3 ( Condition  = MyBaseType2 ( ParamId=~/Foo4 ParamValue=~/Foo5 ) Descriptor = MyBaseType3 ( Baz3 = \'Lorem3\' Baz4 = Lorem4 ) ) ] ), ] ) '
        result = converter.convert_ndf_text(text) 
        assert len(result[0]['Modules']) == 1
        assert result[0]['Modules'][0]['_type_name'] == 'Foo'
        assert result[0]['Modules'][0]['Default']['_base_type_name'] == 'Bar'
        assert result[0]['Modules'][0]['Default']['Baz'] == 'Lorem1'
        assert result[0]['Modules'][0]['Default']['Baz2'] == 'Lorem2'
        assert len(result[0]['Modules'][0]['Selection']) == 2
        assert result[0]['Modules'][0]['Selection'][0] == 'Foo2'
        assert result[0]['Modules'][0]['Selection'][1]['_type_name'] == 'Foo3'
        assert result[0]['Modules'][0]['Selection'][1]['Condition']['ParamId'] == '~/Foo4'
        assert result[0]['Modules'][0]['Selection'][1]['Condition']['ParamValue'] == '~/Foo5'
        assert result[0]['Modules'][0]['Selection'][1]['Descriptor']['Baz3'] == 'Lorem3'
        assert result[0]['Modules'][0]['Selection'][1]['Descriptor']['Baz4'] == 'Lorem4'

    # def test_no_spaces_before_after_array(self, converter):
    #    text = '\n  export Foo is Bar \n ( Baz = [~Foo2] ) '
    #    result = converter.convert_ndf_text(text) 
    #    assert len(result[0]['Baz']) == 1
    #    assert result[0]['Baz'][0] == "~Foo2"

    def test_funny_expressions_as_string_field_values(self, converter):
        text = '\n  export Foo is Bar \n ( Baz = ((80) * Metre) ) '
        result = converter.convert_ndf_text(text) 
        assert result[0]['Baz'] == "((80) * Metre)"

    def test_another_funny_expressions_as_string_field_values(self, converter):
        text = '\n  export Foo is Bar \n ( Baz = (0 * Seconde) ) '
        result = converter.convert_ndf_text(text) 
        assert result[0]['Baz'] == "(0 * Seconde)"

    def test_inlined_objects(self, converter):
        text = '\n  export Foo is Bar \n ( Baz = BazBaseType(Foo2=~/Bar2  Foo3=~/Bar3) ) '
        result = converter.convert_ndf_text(text) 
        assert result[0]['Baz']['_base_type_name'] == 'BazBaseType'
        assert result[0]['Baz']['Foo2'] == "~/Bar2"
        assert result[0]['Baz']['Foo3'] == "~/Bar3"

    def test_flag_list_like_objects(self, converter):
        text = '\n export Foo is Bar \n ( Baz = [ Foo2 ( Bar2 = [ FooListItem, FooListItem2, FooListItem3, FooListItem4 ] ), ] ) '
        result = converter.convert_ndf_text(text)
        assert result[0]['Baz'][0]['_type_name'] == "Foo2"
        assert result[0]['Baz'][0]['Bar2'][0] == "FooListItem"
        assert result[0]['Baz'][0]['Bar2'][1] == "FooListItem2"
        assert result[0]['Baz'][0]['Bar2'][2] == "FooListItem3"
        assert result[0]['Baz'][0]['Bar2'][3] == "FooListItem4"
    

    def test_strings_before_and_after_flag_list_like_objects(self, converter):
        text = '\n export Foo is Bar \n ( Baz = [ Lorem, Foo2 ( Bar2 = [ FooListItem, FooListItem2, FooListItem3, FooListItem4 ] ), Ipsum, Dolor, Sit, Amet, ] ) '
        result = converter.convert_ndf_text(text)

        assert result[0]['Baz'][0] == "Lorem"

        assert result[0]['Baz'][1]['_type_name'] == "Foo2"
        assert result[0]['Baz'][1]['Bar2'][0] == "FooListItem"
        assert result[0]['Baz'][1]['Bar2'][1] == "FooListItem2"
        assert result[0]['Baz'][1]['Bar2'][2] == "FooListItem3"
        assert result[0]['Baz'][1]['Bar2'][3] == "FooListItem4"

        assert result[0]['Baz'][2] == "Ipsum"
        assert result[0]['Baz'][3] == "Dolor"
        assert result[0]['Baz'][4] == "Sit"
        assert result[0]['Baz'][5] == "Amet"

    def test_empty_maps(self, converter):
        text = '\n export Foo is Bar \n ( Baz = MAP [] ) '
        result = converter.convert_ndf_text(text)
        
        assert isinstance(result[0]['Baz'], dict)
        assert len(result[0]['Baz']) == 0
    
    def test_empty_maps2(self, converter):
        text = '\n export Foo is Bar \n ( Baz = MAP [ ] ) '
        result = converter.convert_ndf_text(text)
        
        assert isinstance(result[0]['Baz'], dict)
        assert len(result[0]['Baz']) == 0

    def test_mapped_values(self, converter):
        text = '\n export Foo is Bar \n ( Baz = MAP [ ( Lorem/Ipsum, Dolor Sit Amet ), ( Lorem/Ipsum2, Dolor Sit Amet2 ), ] ) '
        result = converter.convert_ndf_text(text)
        
        assert result[0]['Baz']['Lorem/Ipsum'] == "Dolor Sit Amet"
        assert result[0]['Baz']['Lorem/Ipsum2'] == "Dolor Sit Amet2"
        assert len(result[0]['Baz']) == 2

    
    def test_compressed_mapped_values(self, converter):
        text = '\n export Foo is Bar \n ( Baz = MAP [ (Lorem/Ipsum, Dolor Sit Amet), (Lorem/Ipsum2, Dolor Sit Amet2), ] ) '
        result = converter.convert_ndf_text(text)
        
        assert result[0]['Baz']['Lorem/Ipsum'] == "Dolor Sit Amet"
        assert result[0]['Baz']['Lorem/Ipsum2'] == "Dolor Sit Amet2"
        assert len(result[0]['Baz']) == 2
        