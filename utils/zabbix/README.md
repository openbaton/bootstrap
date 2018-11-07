# Zabbix for Open Baton

Zabbix is the main monitoring system used by Open Baton. It is used to monitor VMs that are managed by the Generic VNF Manager that takes care of the installation and configuration of the Zabbix agent. 

The Zabbix monitoring plugin allows the Open Baton components to retrieve measurements or alarms and enables further processing of those. For instance, it Zabbix is used by the Autoscaling Engine and Fault Management System. Nevertheless, it allows also the simple monitoring of VMs.

Requirements:
* Zabbix Server (version: alpine-3.4.10)
* Zabbix Apache Frontend (version: alpine-3.4.10)
* Mysql Server (version: 5.7)

## Installation
This folder contains a `docker-compose.yml` that can be used to bring up the Zabbix monitoring system. Therefore, go to this folder and just execute the following component:

```bash
docker-compose up -d
```

**Note** The Zabbix server must be reachable by the VMs.

**Note** Further configuration is required in order to monitor VMs automatically. Check the [next section](#configuration).

## Configuration

Once Zabbix monitoring system is up and running, it must be configured to activate the following things: 

1) Auto registration: VMs will get registered automatically in Zabbix without any manual action.
2) Active monitoring: Zabbix uses passive monitoring by default. We change this to active monitoring so that the VMs push their values to Zabbix instead of getting polled by Zabbix.

Both can't be automated and must be done via the dashboard directly. Below the information how to access the dashboard by default:
* URL: http://<HOST_IP>:80
* username: Admin
* password: zabbix

### Auto registration
Can be easily achieved by following the steps below:
1. Click `Configuration -> Actions`
2. Select `Event source: "Auto registration"` 
3. Click `Create action`
4. Enter `Name: "Auto registration"`
5. Click `Operations`
6. Create a new Operation by clicking `New`
7. Select `Operation type: "Link to template"`
8. Select a template by clicking `Select`
9. Typically, we use `Template OS Linux` here by checking the box and pressing `Select`
10. Press `Add` to add the newly created Operation
11. Press `Add` to add the new action

Now you should see the new action with Status *Enabled*. From now on the VMs should be registered automatically.

### Active monitoring
We just have to change from *Passive* to *Active* monitoring by updating the default template, which is typically *Template OS Linux*. Please follow these steps:
1. Click `Configuration -> Templates`
2. Click on the name of your default template. Typically, this is `Template OS Linux`
3. Change to the *Items* by clicking `Items`
4. Select all template's items (not the items of other templates that is indicated in the name) and click `Mass update` at the buttom of the page
5. Select `Type` and select `Zabbix agent (active)` in the drop down menu. Then click `Update` at the buttom

Now it is active monitoring enabled. Keep in mind that the VMs must be able to reach Zabbix server.
