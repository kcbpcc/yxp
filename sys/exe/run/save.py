                    elif (
                        row['source'] == 'positions' and
                        row['product'] == 'MIS' and
                        row['qty'] < 0 and
                        (row['PnL%'] > row['PXY'])
                    ):
                        # Print the row before placing the order
                        print(row)
    
                        try:
                            is_placed = mis_order_buy(key, row)
                            if is_placed:
                                # Write the row to the CSV file here
                                with open(csv_file_path, 'a', newline='') as csvfile:
                                    csvwriter = csv.writer(csvfile)
                                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                        except InputException as e:
                            # Handle the specific exception and print only the error message
                            print(f"An error occurred while placing an order for key {key}: {e}")
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
    
        except Exception as e:
            # Handle any other exceptions that may occur during the loop
            print(f"An unexpected error occurred: {e}")
