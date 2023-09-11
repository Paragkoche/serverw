import asyncio
import logging
import websockets
from ocpp.v16 import ChargePoint as cp 
from ocpp.routing import on
from ocpp.v16 import datatypes,enums,call_result,call
import datetime
logging.basicConfig(level=logging.DEBUG)
def generate_expiry_datetime(days=30):
    current_datetime = datetime.datetime.now()
    expiry_datetime = current_datetime + datetime.timedelta(days=days)
    return expiry_datetime
class ChargePoint (cp):
    @on("BootNotification")
    async def  on_boot_notification(self,**kwargs):
         
        return call_result.BootNotificationPayload(
            current_time=datetime.datetime.utcnow().isoformat(),
            interval=10,
            status=enums.RegistrationStatus.accepted
        )

    
    @on("Authorize")
    async def on_authorize(self):
        return call_result.AuthorizePayload(
            id_tag_info={
                "status":enums.AuthorizationStatus.accepted
            }
        )
    
    @on("CancelReservation")
    async def on_cancel_reservation(self):
        return call_result.CancelReservationPayload(
            status=enums.CancelReservationStatus.accepted
        )
    
    @on("ChangeAvailability")
    async def on_change_availability(self):
        return call_result.ChangeAvailabilityPayload()
    

    @on("ChangeConfiguration")
    async def on_change_configuration(self):
        return call_result.ChangeConfigurationPayload()

    @on("ClearCache")
    async def on_clear_cache(self):
        return call_result.ClearCachePayload()

    @on("ClearCacheProfile")
    async def on_clear_cache_profile(self):
        return call_result.ClearChargingProfilePayload()
    
    @on("DataTransfer")
    async def on_data_transfer(self):
        return call_result.DataTransferPayload()
    
    @on("DiagnosticsStatusNotification")
    async def on_diagnostics_status_notification(self):
        return call_result.DiagnosticsStatusNotificationPayload()

    @on("FirmwareStatusNotification")
    async def on_firmware_status_notification(self):
        return call_result.FirmwareStatusNotificationPayload()

    

    @on("GetConfiguration")
    async def on_get_configuration(self):
        return call_result.GetConfigurationPayload()

    @on("GetDiagnostics")
    async def on_get_diagnostics(self):
        return call_result.GetDiagnosticsPayload()

    @on("GetLocalListVersion")
    async def on_get_local_list_version(self):
        return call_result.GetLocalListVersionPayload()

    @on("Heartbeat")
    async def on_heart_beat(self):
        return call_result.HeartbeatPayload(
            current_time=datetime.datetime.utcnow().isoformat()
        )

    @on("MeterValues")
    async def on_meter_values(self):
        return call_result.MeterValuesPayload()
    
    @on("RemoteStartTransaction")
    async def on_remoter_start_transaction(self):
        return call_result.RemoteStartTransactionPayload()

    @on("RemoteStopTransaction")
    async def on_remote_stop_transaction(self):
        return call_result.RemoteStopTransactionPayload()
    @on("ReserveNow")
    async def on_reserve_now(self):
        return call_result.ReserveNowPayload()
    @on("Reset")
    async def on_reset(self):
        return call_result.ResetPayload()
    @on("SendLocalList")
    async def on_send_local_list(self):
        return call_result.SendLocalListPayload()
    

    @on("StartTransaction")
    async def on_start_transaction(self):
        return call_result.StartTransactionPayload()
    
    @on("StopTransaction")
    async def on_stop_transaction(self):
        return call_result.StopTransactionPayload()
    
    @on("TriggerMessage")
    async def on_trigger_message(self):
        return call_result.TriggerMessagePayload()


    @on("UnlockConnector")
    async def on_unlock_connector(self):
       return call_result.UnlockConnectorPayload()
    

    @on("UpdateFirmware")
    async def on_update_firmware(self):
        return call_result.UpdateFirmwarePayload()
    
async def on_connect(websocket, path):
    try:
        requested_protocols = websocket.request_headers[
            'Sec-WebSocket-Protocol']
    except KeyError:
        logging.info("Client hasn't requested any Subprotocol. "
                 "Closing Connection")
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        
        logging.warning('Protocols Mismatched | Expected Subprotocols: %s,'
                        ' but client supports  %s | Closing connection',
                        websocket.available_subprotocols,
                        requested_protocols)
        return await websocket.close()

    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)

    await cp.start()

async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp2.0.1']
    )
    logging.info("WebSocket Server Started")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())