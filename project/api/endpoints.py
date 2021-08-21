from .common.utils import price_fiat_conversion, price_direct_conversion, parse_direct_conversion

def getConversionRate(reqargs:dict):
        """
        """
        DOUBLE_CONVERSION_FIAT  = [
            'XOF'
        ]

        from_money = reqargs.get("from")
        to_money = reqargs.get("to")
        amount = reqargs.get("amount")
        # For CFA convert into EUR, then in XOF
        if (from_money in DOUBLE_CONVERSION_FIAT) and (to_money in DOUBLE_CONVERSION_FIAT):
            # 1: amount from_money --> result USD fiat-conversion
            result_index = price_fiat_conversion(from_money, 'USD') # auto-parse in utils module
            result = float(result_index)*float(reqargs.get("amount"))
            # 2: result USD --> output to_money fiat-conversion
            output_index = price_fiat_conversion('USD', to_money)
            # output = float(output_index)*float(result)
            amount = result
        else:
            if from_money in DOUBLE_CONVERSION_FIAT:
                # 1: amount from_money --> result USD fiat-conversion
                result_index = price_fiat_conversion(from_money, 'USD')
                result = float(result_index)*float(reqargs.get("amount"))
                # 2: result USD --> output to_money direct-conversion
                output_index = parse_direct_conversion(price_direct_conversion('USD', to_money))
                # output = float(output_index)*float(result)
                amount = result
            elif to_money in DOUBLE_CONVERSION_FIAT:
                # 1: amount from_money --> result USD direct-conversion
                result_index = parse_direct_conversion(price_direct_conversion(from_money, 'USD'))
                result = float(result_index)*float(reqargs.get("amount"))
                # 2: result USD --> output to_money fiat-conversion
                output_index = price_fiat_conversion('USD', to_money)
                # output = float(output_index)*float(result)
                amount = result
            else:
                # direct conversion
                output_index = parse_direct_conversion(price_direct_conversion(from_money, to_money))
                # output = float(output_index)*float(reqargs.get("amount"))
                
        output = float(output_index)*float(amount)
       
        return {
            "output-value": output
        }